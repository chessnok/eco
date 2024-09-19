import telebot
from telebot import types
from django.conf import settings
from core.models import BotUser, \
    BotTicket

TOKEN = settings.TELEGRAM_BOT_TOKEN
bot = telebot.TeleBot(TOKEN)

OPERATOR_CHAT_ID = settings.TELEGRAM_CHAT_ID


# Команда /start
@bot.message_handler(commands=['start'])
def start_message(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

    if message.chat.type == "private":
        btn_location = types.KeyboardButton("📍 Отправить координаты",
                                            request_location=True)
        markup.add(btn_location)

    btn_support = types.KeyboardButton("🆘 Техподдержка")
    btn_event = types.KeyboardButton("🗓️ Добавить мероприятие")
    markup.add(btn_support, btn_event)

    bot.send_message(message.chat.id,
                     "Привет! Вы можете отправить мне свои координаты, обратиться в техподдержку или добавить свое мероприятие.",
                     reply_markup=markup)


# Обработка нажатия на кнопку "Техподдержка"
@bot.message_handler(func=lambda message: message.text == "🆘 Техподдержка")
def support_request(message):
    user_id = message.from_user.id

    # Находим или создаем пользователя бота
    bot_user, created = BotUser.objects.get_or_create(tg_id=user_id)

    # Проверяем, есть ли открытые тикеты для этого пользователя
    open_ticket = BotTicket.objects.filter(bot_user=bot_user,
                                           mark__isnull=True).first()

    if open_ticket:
        bot.send_message(message.chat.id,
                         "У вас уже есть открытый тикет. Пожалуйста, дождитесь ответа оператора.")
    else:
        # Создаем новый тикет
        new_ticket = BotTicket.objects.create(bot_user=bot_user)
        bot.send_message(message.chat.id,
                         "Опишите вашу проблему, и оператор скоро ответит.")


# Обработка сообщений пользователей для описания проблемы
@bot.message_handler(func=lambda message: BotTicket.objects.filter(
    bot_user__tg_id=message.from_user.id, mark__isnull=True).exists())
def receive_support_message(message):
    user_id = message.from_user.id
    bot_user = BotUser.objects.get(tg_id=user_id)

    # Получаем открытый тикет
    open_ticket = BotTicket.objects.filter(bot_user=bot_user,
                                           mark__isnull=True).first()

    if open_ticket:
        # Сохраняем проблему пользователя
        open_ticket.problem = message.text
        open_ticket.save()
        bot.send_message(message.chat.id,
                         "Ваш запрос отправлен оператору. Ожидайте ответа.")

        # Отправляем оператору уведомление с данными пользователя
        user_info = (f"ID: `{user_id}`\n"
                     f"Никнейм: @{message.from_user.username}\n"
                     f"Номер тикета: #{open_ticket.id}")
        bot.send_message(OPERATOR_CHAT_ID, user_info)

        # Пересылаем сообщение пользователя оператору
        bot.forward_message(OPERATOR_CHAT_ID, message.chat.id,
                            message.message_id)


# Оператор отвечает пользователю через команду /reply user_id сообщение
@bot.message_handler(commands=['reply'])
def reply_to_user(message):
    try:
        args = message.text.split(maxsplit=2)
        user_id = int(args[1])
        response = args[2]

        bot_user = BotUser.objects.get(tg_id=user_id)
        open_ticket = BotTicket.objects.filter(bot_user=bot_user,
                                               mark__isnull=True).first()

        if open_ticket:
            bot.send_message(user_id, f"Ответ оператора: {response}")
            bot.send_message(message.chat.id,
                             f"Ответ отправлен пользователю {user_id}.")
        else:
            bot.send_message(message.chat.id,
                             "Тикет уже закрыт или не существует.")
    except Exception as e:
        bot.send_message(message.chat.id, f"Ошибка: {e}")


# Оператор закрывает тикет через команду /close user_id
@bot.message_handler(commands=['close'])
def close_ticket(message):
    try:
        args = message.text.split(maxsplit=1)
        user_id = int(args[1])

        bot_user = BotUser.objects.get(tg_id=user_id)
        open_ticket = BotTicket.objects.filter(bot_user=bot_user,
                                               mark__isnull=True).first()

        if open_ticket:
            open_ticket.mark = 0  # Обозначаем тикет как закрытый без оценки
            open_ticket.save()

            # Добавляем кнопки для оценки работы оператора
            markup = types.InlineKeyboardMarkup()
            for i in range(1, 6):
                markup.add(types.InlineKeyboardButton(str(i),
                                                      callback_data=f"rate_{user_id}_{i}"))

            bot.send_message(user_id,
                             "Ваш тикет был закрыт оператором. Пожалуйста, оцените работу оператора от 1 до 5.",
                             reply_markup=markup)
            bot.send_message(message.chat.id,
                             f"Тикет пользователя {user_id} закрыт.")
        else:
            bot.send_message(message.chat.id,
                             "Тикет уже закрыт или не существует.")
    except Exception as e:
        bot.send_message(message.chat.id, f"Ошибка: {e}")


# Обработка оценки оператора (через callback_data)
@bot.callback_query_handler(func=lambda call: call.data.startswith('rate_'))
def handle_rating(call):
    try:
        data = call.data.split('_')
        user_id = int(data[1])
        rating = int(data[2])

        bot_user = BotUser.objects.get(tg_id=user_id)
        closed_ticket = BotTicket.objects.filter(bot_user=bot_user,
                                                 mark=0).first()

        if closed_ticket:
            closed_ticket.mark = rating
            closed_ticket.save()
            bot.send_message(call.message.chat.id,
                             f"Спасибо за вашу оценку: {rating}!")
        else:
            bot.send_message(call.message.chat.id,
                             "Тикет уже закрыт или не существует.")
    except Exception as e:
        bot.send_message(call.message.chat.id, f"Ошибка: {e}")

    bot.answer_callback_query(call.id)

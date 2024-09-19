# core/tasks.py
from datetime import timedelta
from django.utils import timezone
from django.utils.timezone import now
from haversine import haversine

from core.models import BotUser, Event
from telebot import TeleBot
from django.conf import settings

from eco.celery import app

bot = TeleBot(settings.TELEGRAM_BOT_TOKEN)


@app.task
def send_event_reminders():
    today = timezone.now().date()

    reminder_dates = [
        today + timedelta(days=3),
        today + timedelta(days=2),
        today + timedelta(days=1),
    ]

    # Найдем пользователей с координатами
    users_with_location = BotUser.objects.filter(has_location=True)

    for event in Event.objects.filter(date__in=reminder_dates,
                                      is_published=True):
        event_location = (event.latitude, event.longitude)

        for user in users_with_location:
            user_location = (user.latitude, user.longitude)
            distance = haversine(event_location, user_location)

            if distance <= 30:
                days_left = (event.date - today).days
                bot.send_message(
                    user.tg_id,
                    f"Напоминание: Мероприятие '{event.name}' состоится через {days_left} день(дня). Описание: {event.description}"
                )

@app.task
def generate_promo_codes_for_tomorrow_events():
    tomorrow = now().date() + timedelta(days=1)
    events = Event.objects.filter(date=tomorrow, promo_codes__isnull=True)

    for event in events:
        event.generate_promo_codes()
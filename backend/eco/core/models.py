from math import floor

from django.contrib.auth.models import User, AbstractUser
from django.core import validators
from django.db import models
from django.utils.translation import gettext_lazy as _
from haversine import haversine


class PromoCodeUsage(models.Model):
    user = models.ForeignKey("UserModel", on_delete=models.CASCADE,
                             related_name="used_promocodes")
    promo_code = models.OneToOneField("core.PromoCode", on_delete=models.CASCADE,
                                      related_name="usage")
    activated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} used {self.promo_code.code}"

def generate_code():
    import random
    import string
    return ''.join(
        random.choices(string.ascii_uppercase + string.digits, k=10))



class PromoCode(models.Model):
    code = models.CharField(max_length=20)
    discount = models.IntegerField(default=0)
    event = models.ForeignKey("Event", on_delete=models.CASCADE,
                              related_name="promo_codes")

    def __str__(self):
        return self.code

    def activate(self, user):
        """Активировать промокод и добавить его номинал на баланс пользователя."""
        if PromoCodeUsage.objects.filter(promo_code=self).exists():
            raise ValueError("Этот промокод уже был использован.")

        # Создаем запись об использовании промокода
        PromoCodeUsage.objects.create(user=user, promo_code=self)

        # Увеличиваем баланс пользователя
        user.balance += self.discount
        user.save()

        return self.discount

    def __init__(self, *args, **kwargs):
        self.code = generate_code()
        super().__init__(*args, **kwargs)

class Event(models.Model):
    STATUS_CHOICES = [
        ('scheduled', _('Запланировано')),
        ('canceled', _('Отменено')),
        ('finished', _('Завершено')),
    ]

    name = models.CharField(max_length=100)
    date = models.DateField()
    description = models.TextField()
    location = models.CharField(max_length=255)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES,
                              default='scheduled')
    is_published = models.BooleanField(default=False)
    latitude = models.FloatField(null=True, blank=True)  # Добавляем широту
    longitude = models.FloatField(null=True, blank=True)  # Добавляем долготу
    organizer = models.ForeignKey("events.Organizer",
                                  on_delete=models.RESTRICT, null=False,
                                  blank=False, related_name='events')
    participants = models.ManyToManyField("UserModel",
                                          related_name='participated_events',
                                          blank=True)

    def generate_promo_codes(self):
        """Generate promo codes for the event."""
        participants_count = self.participants_count
        promo_code_count = max(1,
                               participants_count // 10)  # Кол-во промокодов, минимум 1
        discount_amount = floor(10000 / promo_code_count)  # Сумма скидки

        # Генерация промокодов
        for _ in range(promo_code_count):
            PromoCode.objects.create(
                code=generate_code(),
                discount=discount_amount,
                event=self
            )

    @property
    def participants_count(self):
        return self.participants.count()

    def __str__(self):
        return self.name

    def get_distance(self, latitude, longitude):
        event_location = (self.latitude, self.longitude)
        user_location = (latitude, longitude)
        return haversine(event_location, user_location)


class UserModel(AbstractUser):
    age = models.PositiveIntegerField(null=True, blank=True)
    home_address = models.CharField(max_length=255, blank=True)
    is_organizer = models.BooleanField(default=False)
    balance = models.IntegerField(default=0)

    def __str__(self):
        return self.username


class BotUser(models.Model):
    id = models.AutoField(primary_key=True)
    longitude = models.FloatField(null=True, blank=True)
    latitude = models.FloatField(null=True, blank=True)
    has_location = models.BooleanField(default=False)
    tg_id = models.IntegerField()

    def __str__(self):
        return f"Пользователь бота {self.tg_id}"


class BotTicket(models.Model):
    id = models.AutoField(primary_key=True)
    bot_user = models.ForeignKey(BotUser, on_delete=models.CASCADE)
    mark = models.IntegerField(null=True, blank=True, default=None,
                               validators=[
                                   validators.MinValueValidator(1),
                                   validators.MaxValueValidator(5)
                               ])

    def __str__(self):
        return f"Тикет от {self.bot_user.tg_id}"

from django.contrib.auth.models import User, AbstractUser
from django.core import validators
from django.db import models
from django.utils.translation import gettext_lazy as _
from haversine import haversine


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

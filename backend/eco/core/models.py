from django.contrib.auth.models import User, AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _




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

    def __str__(self):
        return self.name


class UserModel(AbstractUser):
    age = models.PositiveIntegerField(null=True, blank=True)
    home_address = models.CharField(max_length=255, blank=True)
    is_organizer = models.BooleanField(default=False)

    def __str__(self):
        return self.username

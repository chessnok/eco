from datetime import datetime

from django.conf import settings
from django.core.validators import RegexValidator
from django.db import models

from core.models import UserModel


class Organizer(models.Model):
    STATUS_CHOICES = [
        ('WaitingForConfirmation', 'Ожидает проверки администратором'),
        ('Confirmed', 'Проверенна организатором'),
        ('Rejected', 'Отклоненно администратором'),
    ]
    user = models.OneToOneField(UserModel, on_delete=models.CASCADE)
    organization_name = models.CharField(max_length=255)
    ogrn = models.CharField(max_length=13,
                            validators=[RegexValidator(r'^\d{13}$')])
    documents = models.FileField(upload_to='org_docs/')
    status = models.CharField(max_length=50, choices=STATUS_CHOICES,
                              default='WaitingForConfirmation')
    created_at = models.DateTimeField(auto_now_add=True)
    registration_date = models.DateField(null=True, blank=True)
    org_type = models.CharField(max_length=255, null=True, blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)
    data_fetched_at = models.DateTimeField(null=True, blank=True)

    def fetch_api_data(self):
        req = self.ogrn
        url = f"https://api-fns.ru/api/egr?req={req}&key={settings.ORGANIZATIONS_API_KEY}"
        import requests
        response = requests.get(url)
        if not response.ok:
            raise Exception(
                'Ошибка при запросе к API с данными об организации')
        data = response.json()
        if len(data['items']) == 0:
            raise Exception('Организация с таким ОГРН не найдена')
        data = data['items'][0]['ЮЛ']
        self.registration_date = datetime.strptime(data['ДатаОГРН'],
                                                   '%Y-%m-%d')
        self.organization_name = data['НаимПолнЮЛ']
        self.org_type = data['ОКОПФ']
        self.address = data['Адрес']['АдресПолн']
        self.data_fetched_at = datetime.now()

    def save(self, *args, **kwargs):
        is_init = not self.pk
        if is_init:
            self.fetch_api_data()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Организатор: {self.organization_name} ({self.user.username})"

    class Meta:
        verbose_name = 'Организатор'
        verbose_name_plural = 'Организаторы'

    @property
    def events_list(self):
        return self.events.all()

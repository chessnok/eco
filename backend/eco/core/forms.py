from datetime import datetime

from django import forms
from django.contrib.auth.forms import UserCreationForm

from core.models import UserModel, Event, PromoCode


class CustomUserCreationForm(UserCreationForm):
    age = forms.IntegerField(required=False, label='Age')
    home_address = forms.CharField(required=False, label='Home Address')

    class Meta:
        model = UserModel
        fields = ('username', 'email', 'password1', 'password2', 'first_name',
                  'last_name', 'age', 'home_address')


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserModel
        fields = ('first_name', 'last_name', 'email', 'age', 'home_address')
        widgets = {
            'age': forms.NumberInput(attrs={'min': 0}),
            'home_address': forms.TextInput(attrs={'id': 'address-input'}),
        }


class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ('name', 'sex', 'age', 'image', 'date', 'description', 'longitude', 'latitude')
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'description': forms.Textarea(attrs={'rows': 3}),
        }

    def clean_date(self):
        date = self.cleaned_data.get('date')
        if date < datetime.now().date():
            raise forms.ValidationError('Дата не может быть в прошлом.')
        return date

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)  # Получаем пользователя из kwargs
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        event = super().save(commit=False)
        event.organizer = self.user.organizer  # Устанавливаем организатора
        if commit:
            event.save()
        return event


class PromoCodeActivationForm(forms.Form):
    code = forms.CharField(max_length=20, label="Промокод")

    def clean_code(self):
        code = self.cleaned_data['code']
        try:
            promo_code = PromoCode.objects.get(code=code)
        except PromoCode.DoesNotExist:
            raise forms.ValidationError("Промокод не найден.")
        return promo_code

from django import forms
from django.contrib.auth.forms import UserCreationForm

from core.models import UserModel, Event


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
        fields = ('name', 'date', 'description', 'location')
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'description': forms.Textarea(attrs={'rows': 3}),
        }

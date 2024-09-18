from django import forms
from .models import Organizer


class OrganizerRegistrationForm(forms.ModelForm):
    class Meta:
        model = Organizer
        fields = ['ogrn', 'documents']

    def clean_ogrn(self):
        ogrn = self.cleaned_data.get('ogrn')
        if len(ogrn) != 13:
            raise forms.ValidationError('ОГРН должен содержать 13 цифр.')
        return ogrn

from django import forms
from .models import CzatOgolny

class CzatOgolnyForm(forms.ModelForm):
    class Meta:
        model = CzatOgolny
        fields = ['tresc_wiadomosci']

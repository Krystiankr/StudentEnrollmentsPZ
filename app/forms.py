from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm

from .models import CzatOgolny


class CzatOgolnyForm(forms.ModelForm):
    class Meta:
        model = CzatOgolny
        fields = ['tresc_wiadomosci']

class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["username", "email"]

class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))

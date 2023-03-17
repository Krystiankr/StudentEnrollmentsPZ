from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm

from .models import CzatOgolny, Studenci


class CzatOgolnyForm(forms.ModelForm):
    class Meta:
        model = CzatOgolny
        fields = ["tresc_wiadomosci"]


class NewUserForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("first_name", "last_name", "email", "password1", "password2")

    def save(self, commit=True):
        user = super(NewUserForm, self).save(commit=False)
        user.email = self.cleaned_data["email"]
        user.username = (
            f'{self.cleaned_data["first_name"]}.{self.cleaned_data["last_name"]}'
        )
        if commit:
            user.save()
        student = Studenci(user=user, imie=self.cleaned_data["first_name"], nazwisko=self.cleaned_data["last_name"])
        student.save()
        return user


class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control"}))
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={"class": "form-control"})
    )
    #
    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     del self.fields['username']
    #

from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

from account.models import User


class RegisterUserForm(UserCreationForm):
    nickname = forms.CharField(label="Ваш ник", widget=forms.TextInput(attrs={'class': 'form-input form-control mt-2'}))
    email = forms.CharField(label="Ваша почта", widget=forms.EmailInput(attrs={'class': 'form-input form-control mt-2'}))
    password1 = forms.CharField(label="Пароль", widget=forms.PasswordInput(attrs={'class': 'form-input form-control mt-2'}))
    password2 = forms.CharField(label="Повтор пароля", widget=forms.PasswordInput(attrs={'class': 'form-input form-control mt-2'}))

    class Meta:
        model = User
        fields = ("nickname", "email", "password1", "password2")


class LoginUserForm(AuthenticationForm):
    username = forms.CharField(label="Логин(Ваша почта)", widget=forms.TextInput(attrs={'class': 'form-input form-control mt-2'}))
    password = forms.CharField(label="Пароль", widget=forms.PasswordInput(attrs={'class': 'form-input form-control mt-2'}))
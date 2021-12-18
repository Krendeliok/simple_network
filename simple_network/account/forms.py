from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UserChangeForm

from account.models import Post, User


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

class SettingsForm(forms.Form):
    nickname = forms.CharField(label="Ваш ник", widget=forms.TextInput(attrs={'class': 'form-input form-control mt-2'}))
    email = forms.CharField(label="Ваша почта", widget=forms.EmailInput(attrs={'class': 'form-input form-control mt-2'}))
    password = forms.CharField(label="Пароль", required=False, widget=forms.PasswordInput(attrs={'class': 'form-input form-control mt-2'}))
    repeat_password = forms.CharField(label="Повтор пароля", required=False, widget=forms.PasswordInput(attrs={'class': 'form-input form-control mt-2'}))
    photo = forms.ImageField(label="Фото профиля", required=False, widget=forms.FileInput(attrs={'class': 'form-input form-control mt-2'}))

    class Meta:
        model = User
        fields = ("nickname", "email", "password", "repeat_password", "photo")

class AddPostForm(forms.Form):
    post_text = forms.CharField(label="Текст поста", widget=forms.Textarea(attrs={'class': 'form-input form-control mt-2'}))
    
    class Meta:
        model = Post
        fields = ("post_text")

class SearchForm(forms.Form):
    search_field = forms.CharField(label="Поиск", required=False, widget=forms.TextInput(attrs={'class': 'form-input form-control mt-2', 'placeholder': 'Введите ник пользователя'}))
    
    class Meta:
        fields = ("search_field")
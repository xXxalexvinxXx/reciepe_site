# users/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
from .models import UserProfile

# Форма для регистрации нового пользователя
class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')  # Поля для регистрации

    # Добавляем плейсхолдеры
    username = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Введите ваше имя пользователя'})
    )
    first_name = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Введите ваше имя'})
    )
    last_name = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Введите вашу фамилию'})
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'placeholder': 'Введите ваш email'})
    )

# Форма для изменения данных пользователя
class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password')  # Поля для изменения

    # Добавляем плейсхолдеры
    username = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Введите имя пользователя'})
    )
    first_name = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Введите ваше имя'})
    )
    last_name = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Введите вашу фамилию'})
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'placeholder': 'Введите ваш email'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Введите пароль'})
    )

# Форма для редактирования профиля пользователя
class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['avatar']  # Поле для редактирования аватара

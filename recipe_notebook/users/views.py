# users/views.py
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from .forms import CustomUserCreationForm, CustomUserChangeForm, UserProfileForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import logout
from .models import UserProfile

# Регистрация пользователя
def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()  # Сохраняем пользователя
            login(request, user)  # Автоматическая авторизация пользователя
            messages.success(request, "Регистрация успешна! Вы авторизованы.")  # Сообщение об успехе
            return redirect('home')  # Перенаправляем на главную страницу
        else:
            # Если форма невалидна, выводим ошибки
            for field in form.errors:
                messages.error(request, f"Ошибка в поле {field}: {form.errors[field]}")
    else:
        form = CustomUserCreationForm()

    return render(request, 'users/register.html', {'form': form})

# Авторизация пользователя
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')  # Перенаправление на домашнюю страницу
        else:
            # Если форма не прошла валидацию, выводим ошибку
            messages.error(request, 'Ошибка авторизации. Неверный логин или пароль.')  # Добавляем сообщение об ошибке
    else:
        form = AuthenticationForm()

    return render(request, 'users/login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('home')  # Редирект на главную страницу после выхода


# Редактирование профиля пользователя
@login_required
def profile(request):
    try:
        # Пытаемся получить профиль пользователя
        user_profile = request.user.userprofile
    except UserProfile.DoesNotExist:
        # Если профиль не существует, создаем новый
        user_profile = UserProfile.objects.create(user=request.user)

    if request.method == 'POST':
        user_form = CustomUserChangeForm(request.POST, instance=request.user)
        profile_form = UserProfileForm(request.POST, request.FILES, instance=user_profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, "Ваш профиль успешно обновлен!")
            return redirect('profile')
    else:
        user_form = CustomUserChangeForm(instance=request.user)
        profile_form = UserProfileForm(instance=user_profile)

    return render(request, 'users/profile.html', {'user_form': user_form, 'profile_form': profile_form})

from django.contrib import admin
from django.contrib.auth.models import User
from .models import UserProfile

# Регистрируем профиль пользователя
admin.site.register(UserProfile)

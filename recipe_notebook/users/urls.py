# users/urls.py
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views



urlpatterns = [
    path('register/', views.register_view, name='register'),  # Страница регистрации
    path('login/', views.login_view, name='login'),  # Страница входа
    path('profile/', views.profile, name='profile'),  # Страница профиля
    path('logout/', views.logout_view, name='logout'),  # Путь для выхода
]

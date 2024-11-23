from django.urls import path
from . import views

urlpatterns = [
    path('', views.ingredient_list, name='ingredient_list'),  # Список ингредиентов
    path('create/', views.create_ingredient, name='create_ingredient'),  # Добавление ингредиента
    path('<int:pk>/', views.ingredient_detail, name='ingredient_detail'),
]

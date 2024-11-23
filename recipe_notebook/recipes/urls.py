from django.urls import path
from . import views

urlpatterns = [
    path('', views.recipe_list, name='recipe_list'),  # Список рецептов
    path('<int:pk>/', views.recipe_detail, name='recipe_detail'),  # Детальная страница рецепта
    path('add_recipe/', views.add_recipe, name='add_recipe'),  # Добавить рецепт
    path('save_recipe/', views.save_recipe, name='save_recipe'),  # Сохранить рецепт
    path('<int:pk>/edit/', views.edit_recipe, name='edit_recipe'),  # Редактировать рецепт
    path('add_ingredients/', views.add_ingredients, name='add_ingredients'),
    path('delete_ingredient/<int:pk>/', views.delete_ingredient, name='delete_ingredient'),
]

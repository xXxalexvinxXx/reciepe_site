# main/views.py
from django.shortcuts import render
from recipes.models import Recipe
import random

# Главная страница с примерами рецептов
def home(request):
    # Получаем все рецепты из базы данных
    all_recipes = Recipe.objects.all()

    # Если рецептов больше 5, выбираем случайные 5
    if all_recipes.count() > 5:
        recipes = random.sample(list(all_recipes), 5)
    else:
        recipes = all_recipes  # Если рецептов меньше 5, показываем все

    return render(request, 'main/home.html', {'recipes': recipes})
# Страница "О сайте"
def about(request):
    return render(request, 'main/about.html')

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Ingredient, IngredientCategory
from .forms import IngredientForm

# Отображение списка ингредиентов
def ingredient_list(request):
    # Получаем все категории, у которых есть хотя бы один ингредиент
    categories = IngredientCategory.objects.filter(ingredient__isnull=False)

    # Группируем ингредиенты по категориям
    ingredients_by_category = {}
    for category in categories:
        # Для каждой категории находим все связанные ингредиенты
        ingredients_by_category[category] = Ingredient.objects.filter(category=category)

    context = {
        'ingredients_by_category': ingredients_by_category
    }

    return render(request, 'ingredients/ingredient_list.html', context)

# Детальная информация об ингредиенте
def ingredient_detail(request, pk):
    ingredient = get_object_or_404(Ingredient, pk=pk)
    context = {
        'ingredient': ingredient
    }
    return render(request, 'ingredients/ingredient_detail.html', context)

# Добавление нового ингредиента
@login_required
def create_ingredient(request):
    if request.method == 'POST':
        form = IngredientForm(request.POST, request.FILES)
        if form.is_valid():
            # Не сохраняем ингредиент, если пользователь не авторизован
            ingredient = form.save(commit=False)
            # Устанавливаем, что ингредиент был добавлен авторизованным пользователем
            # Но сохраняем его только в случае, если это авторизованный пользователь
            if request.user.is_authenticated:
                ingredient.save()  # Сохраняем новый ингредиент в базе данных
                return redirect('ingredient_list')  # Перенаправляем на страницу списка ингредиентов
            else:
                # Если пользователь не авторизован, не сохраняем ингредиент
                form.add_error(None, 'Вы должны быть авторизованы для добавления ингредиента.')
        else:
            form.add_error(None, 'Форма не прошла валидацию.')

    else:
        form = IngredientForm()

    return render(request, 'ingredients/create_ingredient.html', {'form': form})

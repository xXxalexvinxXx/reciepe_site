from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .forms import IngredientForm, RecipeForm
from .models import Recipe, RecipeIngredient
from ingredients.models import Ingredient, IngredientCategory
from decimal import Decimal
from django.http import HttpResponseForbidden

# Отображение списка рецептов
def recipe_list(request):
    recipes = Recipe.objects.all()
    return render(request, 'recipes/recipe_list.html', {'recipes': recipes})

# Детальная страница рецепта
def recipe_detail(request, pk):
    recipe = get_object_or_404(Recipe, pk=pk)

    # Получаем ингредиенты с их количеством
    ingredients_with_amount = [
        {'ingredient': recipe_ingredient.ingredient, 'amount': recipe_ingredient.amount}
        for recipe_ingredient in RecipeIngredient.objects.filter(recipe=recipe)
    ]

    # Разделяем шаги по точкам и добавляем разрыв строки после каждой точки
    steps = recipe.steps.split('.')  # Разделяем шаги по точке
    steps = [step.strip() + '.' for step in steps if step]  # Убираем лишние пробелы и восстанавливаем

    # Расчет БЖУ и калорий
    bju_and_calories = recipe.calculate_bju_and_calories()

    # Автор рецепта
    is_author = recipe.author == request.user if request.user.is_authenticated else False

    return render(request, 'recipes/recipe_detail.html', {
        'recipe': recipe,
        'ingredients_with_amount': ingredients_with_amount,
        'steps': steps,  # Передаем обработанные шаги в шаблон
        'is_author': is_author,
        'bju_and_calories': bju_and_calories,
    })

# Добавление нового рецепта
@login_required
def add_recipe(request):
    if request.method == 'POST':
        recipe_form = RecipeForm(request.POST, request.FILES)
        if recipe_form.is_valid():
            recipe = recipe_form.save(commit=False)
            # Устанавливаем автора рецепта
            recipe.author = request.user
            recipe.save()

            request.session['current_recipe_id'] = recipe.id
            return redirect('add_ingredients')
    else:
        recipe_form = RecipeForm()

    return render(request, 'recipes/add_recipe.html', {'recipe_form': recipe_form})

# Добавление ингредиентов к рецепту
@login_required
def add_ingredients(request):
    current_recipe_id = request.session.get('current_recipe_id')
    if not current_recipe_id:
        return redirect('add_recipe')

    recipe = Recipe.objects.get(id=current_recipe_id)

    if request.method == 'POST':
        ingredient_form = IngredientForm(request.POST)
        if ingredient_form.is_valid():
            ingredient_data = ingredient_form.cleaned_data
            ingredient_instance = ingredient_data['ingredient']
            amount = ingredient_data['amount']

            ingredients_data = request.session.get('ingredients_data', [])
            ingredients_data.append({'ingredient_id': ingredient_instance.id, 'amount': str(amount)})
            request.session['ingredients_data'] = ingredients_data

            return redirect('add_ingredients')

        if 'save_ingredients' in request.POST:
            ingredients_data = request.session.get('ingredients_data', [])
            for ingredient in ingredients_data:
                ingredient_instance = Ingredient.objects.get(id=ingredient['ingredient_id'])
                RecipeIngredient.objects.create(
                    recipe=recipe,
                    ingredient=ingredient_instance,
                    amount=Decimal(ingredient['amount'])
                )

            request.session['ingredients_data'] = []
            return redirect('save_recipe')
    else:
        ingredient_form = IngredientForm()

    ingredients_data = request.session.get('ingredients_data', [])
    ingredients = [{'ingredient': Ingredient.objects.get(id=data['ingredient_id']), 'amount': data['amount'], 'id': data['ingredient_id']} for data in ingredients_data]

    return render(request, 'recipes/add_ingredients.html', {
        'ingredient_form': ingredient_form,
        'ingredients': ingredients
    })

# Удаление ингредиента из сессии
@login_required
def delete_ingredient(request, ingredient_id):
    ingredients_data = request.session.get('ingredients_data', [])
    ingredients_data = [ingredient for ingredient in ingredients_data if ingredient['ingredient_id'] != str(ingredient_id)]
    request.session['ingredients_data'] = ingredients_data
    return redirect('add_ingredients')

# Получение ингредиентов по категории
def get_ingredients_by_category(request):
    category_id = request.GET.get('category_id')
    if category_id:
        try:
            ingredients = Ingredient.objects.filter(category_id=category_id).values('id', 'name')
            return JsonResponse({'ingredients': list(ingredients)})
        except Exception as e:
            return JsonResponse({'error': str(e), 'ingredients': []})
    return JsonResponse({'ingredients': []})


# Сохранение рецепта как опубликованного
@login_required
def save_recipe(request):
    current_recipe_id = request.session.get('current_recipe_id')
    if not current_recipe_id:
        return redirect('add_recipe')

    recipe = Recipe.objects.get(id=current_recipe_id)
    recipe.published = True  # Устанавливаем флаг опубликованности
    recipe.save()

    request.session['current_recipe_id'] = None  # Очищаем сессию

    return redirect('recipe_detail', pk=recipe.id)

# Редактирование рецепта
@login_required
def edit_recipe(request, pk):
    recipe = get_object_or_404(Recipe, pk=pk)

    # Проверка авторства
    if recipe.author != request.user:
        return HttpResponseForbidden("Вы не можете редактировать чужой рецепт.")

    if request.method == 'POST':
        recipe_form = RecipeForm(request.POST, request.FILES, instance=recipe)
        if recipe_form.is_valid():
            recipe_form.save()
            return redirect('recipe_detail', pk=recipe.id)
    else:
        recipe_form = RecipeForm(instance=recipe)

    return render(request, 'recipes/edit_recipe.html', {'recipe_form': recipe_form, 'recipe': recipe})

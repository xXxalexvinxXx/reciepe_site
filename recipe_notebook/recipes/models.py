import os
import uuid
from django.db import models
from PIL import Image
from ingredients.models import Ingredient
from django.contrib.auth.models import User


# Категория рецепта
class RecipeCategory(models.Model):
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        verbose_name = "Категория рецепта"
        verbose_name_plural = "Категории рецептов"

    def __str__(self):
        return self.name


# Рецепт
class Recipe(models.Model):
    name = models.CharField(max_length=200, unique=True)
    category = models.ForeignKey(RecipeCategory, on_delete=models.CASCADE)
    description = models.TextField()
    image = models.ImageField(upload_to='recipes/', null=True, blank=True)
    difficulty = models.PositiveIntegerField(choices=[(1, '1 звезда'), (2, '2 звезды'), (3, '3 звезды'), (4, '4 звезды'), (5, '5 звезд')])
    ingredients = models.ManyToManyField(Ingredient, through='RecipeIngredient')
    cook_time = models.PositiveIntegerField(help_text="Время приготовления в минутах")
    steps = models.TextField(help_text="Опишите шаги приготовления")
    author = models.ForeignKey(User, on_delete=models.SET_DEFAULT, default=None, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def calculate_bju_and_calories(self):
        total_protein = 0
        total_fat = 0
        total_carbohydrate = 0
        total_calories = 0

        for recipe_ingredient in self.recipeingredient_set.all():
            ingredient = recipe_ingredient.ingredient
            amount = recipe_ingredient.amount  # Количество ингредиента в рецепте в граммах

            # Рассчитываем БЖУ и калории на основе количества
            total_protein += ingredient.protein * amount / 100
            total_fat += ingredient.fat * amount / 100
            total_carbohydrate += ingredient.carbohydrate * amount / 100
            total_calories += ingredient.calories * amount / 100

        return {
            'protein': round(total_protein, 2),
            'fat': round(total_fat, 2),
            'carbs': round(total_carbohydrate, 2),
            'calories': round(total_calories, 2),
        }

    def save(self, *args, **kwargs):
        if not self.author:
            self.author = User.objects.filter(is_superuser=True).first()
        super().save(*args, **kwargs)

        if self.image:
            original_path = self.image.path
            ext = os.path.splitext(self.image.name)[1]  # Расширение файла
            new_name = f"recipe_{uuid.uuid4()}{ext}"  # Уникальное имя файла
            new_path = os.path.join(os.path.dirname(original_path), new_name)

            # Обработка изображения
            with Image.open(original_path) as img:
                img = img.resize((300, 300), Image.Resampling.LANCZOS)
                img.save(new_path)

            # Обновляем путь к изображению в модели
            self.image.name = f"recipes/{new_name}"

            # Удаляем оригинальный файл
            if os.path.exists(original_path):
                os.remove(original_path)

            super().save(update_fields=['image'])

    class Meta:
        verbose_name = "Рецепт"
        verbose_name_plural = "Рецепты"

    def __str__(self):
        return self.name


# Модель ингредиента для рецепта
class RecipeIngredient(models.Model):
    recipe = models.ForeignKey('Recipe', on_delete=models.CASCADE)
    ingredient = models.ForeignKey('ingredients.Ingredient', on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=8, decimal_places=2)

    class Meta:
        verbose_name = "Ингредиент для рецепта"
        verbose_name_plural = "Ингредиенты для рецепта"

    def __str__(self):
        return f'{self.ingredient.name} - {self.amount} г'

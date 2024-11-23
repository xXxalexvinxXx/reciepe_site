from django.contrib import admin
from .models import Ingredient, IngredientCategory

@admin.register(IngredientCategory)
class IngredientCategoryAdmin(admin.ModelAdmin):
    list_display = ['name']

@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'protein', 'fat', 'carbohydrate', 'calories']

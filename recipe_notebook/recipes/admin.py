from django.contrib import admin
from .models import Recipe, RecipeCategory, RecipeIngredient

class RecipeIngredientInline(admin.TabularInline):
    model = RecipeIngredient
    extra = 1

class RecipeAdmin(admin.ModelAdmin):
    inlines = [RecipeIngredientInline]
    list_display = ('name', 'category', 'author', 'created_at', 'updated_at')
    search_fields = ('name', 'description')
    list_filter = ('category',)

admin.site.register(Recipe)
admin.site.register(RecipeCategory)
admin.site.register(RecipeIngredient)

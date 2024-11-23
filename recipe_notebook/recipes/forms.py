from django import forms
from django_select2.forms import Select2Widget
from .models import Recipe
from ingredients.models import Ingredient, IngredientCategory

class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = ['name', 'category', 'description', 'image', 'difficulty', 'cook_time', 'steps']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
            'steps': forms.Textarea(attrs={'rows': 5}),  # Текстовое поле для шагов
        }
        labels = {
            'cook_time': 'Время приготовления (минуты)',
            'steps': 'Шаги приготовления',
        }




class IngredientForm(forms.Form):
    ingredient = forms.ModelChoiceField(
        queryset=Ingredient.objects.all(),
        widget=Select2Widget(attrs={'data-placeholder': 'Выберите ингредиент...'}),
        label='Ингредиент'
    )
    amount = forms.DecimalField(label='Количество (г)', max_digits=10, decimal_places=2)
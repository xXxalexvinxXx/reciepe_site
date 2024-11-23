from django import forms
from .models import Ingredient

class IngredientForm(forms.ModelForm):
    class Meta:
        model = Ingredient
        fields = [
            'name', 'category', 'image',
            'protein', 'fat', 'carbohydrate',
            'calories'
        ]
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Название ингредиента'}),
            'category': forms.Select(attrs={'class': 'category-select'}),
            'image': forms.ClearableFileInput(),
            'protein': forms.NumberInput(attrs={'placeholder': 'Количество белков'}),
            'fat': forms.NumberInput(attrs={'placeholder': 'Количество жиров'}),
            'carbohydrate': forms.NumberInput(attrs={'placeholder': 'Количество углеводов'}),
            'calories': forms.NumberInput(attrs={'placeholder': 'Энергетическая ценность'}),
        }

        def clean_image(self):
            image = self.cleaned_data.get('image')
            if image:
                # Пример переименования файла, если необходимо
                file_name = image.name
            return image

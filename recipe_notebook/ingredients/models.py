import os
import uuid
from django.db import models
from PIL import Image

# Модель категории ингредиентов
class IngredientCategory(models.Model):
    name = models.CharField(
        max_length=100,
        unique=True,
        verbose_name="Категория"
    )  # Название категории, уникальное

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Категория ингредиента"
        verbose_name_plural = "Категории ингредиентов"


# Модель ингредиента
class Ingredient(models.Model):
    name = models.CharField(
        max_length=100,
        unique=True,
        verbose_name="Название"
    )  # Название ингредиента, уникальное
    category = models.ForeignKey(
        IngredientCategory,
        on_delete=models.CASCADE,
        verbose_name="Категория"
    )  # Категория ингредиента
    image = models.ImageField(
        upload_to='ingredients/',
        blank=True,
        null=True,
        verbose_name="Изображение"
    )  # Изображение, необязательное поле
    protein = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="Белки (г/100г)")  # Количество белков
    fat = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="Жиры (г/100г)")  # Количество жиров
    carbohydrate = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="Углеводы (г/100г)")  # Количество углеводов
    calories = models.DecimalField(max_digits=6, decimal_places=2, verbose_name="Калорийность (ккал/100г)")  #
    # Калорийность

    def save(self, *args, **kwargs):
        # Сохраняем объект, чтобы файл изображения появился на диске
        super().save(*args, **kwargs)

        if self.image:
            # Получаем путь к исходному файлу изображения
            original_path = self.image.path
            ext = os.path.splitext(self.image.name)[1]  # Расширение файла
            new_name = f"ingredient_{uuid.uuid4()}{ext}"  # Уникальное имя файла
            new_path = os.path.join(os.path.dirname(original_path), new_name)

            # Обработка изображения
            with Image.open(original_path) as img:
                img = img.resize((300, 300), Image.Resampling.LANCZOS)  # Уменьшаем изображение
                img.save(new_path)  # Сохраняем обработанный файл с новым именем

            # Обновляем путь к изображению в модели
            self.image.name = f"ingredients/{new_name}"

            # Удаляем оригинальный файл
            if os.path.exists(original_path):
                os.remove(original_path)

            # Сохраняем изменения модели
            super().save(update_fields=['image'])

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Ингредиент"
        verbose_name_plural = "Ингредиенты"

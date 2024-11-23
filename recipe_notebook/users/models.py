from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)

    def save(self, *args, **kwargs):
        # Если аватар был изменен, то сжимаем его
        if self.avatar:
            img = Image.open(self.avatar)
            img.thumbnail((300, 300))  # Устанавливаем максимальный размер 300x300
            img.save(self.avatar.path)  # Перезаписываем файл сжатием
        super().save(*args, **kwargs)
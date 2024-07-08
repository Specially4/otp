from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    class Meta:
        verbose_name = 'Пользатель'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username


class QrCode(models.Model):
    class Meta:
        verbose_name = 'QR-код'
        verbose_name_plural = 'QR-коды'

    key = models.CharField(max_length=255, verbose_name='Ключ')
    qr_code_image = models.ImageField(upload_to='qr_codes/', verbose_name='Изображение QR-кода')
    created = models.DateTimeField(verbose_name='Дата создания')
    updated = models.DateTimeField(verbose_name='Дата изменения')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь', related_name='user')

    def __str__(self):
        return self.id

    def save(self, *args, **kwargs):
        if not self.id:
            self.created = timezone.now()
        self.updated = timezone.now()
        return super().save(*args, **kwargs)

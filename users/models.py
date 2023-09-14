from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """Пользователь"""
    avatar = models.ImageField(upload_to='users/', blank=True, null=True, verbose_name='аватар')
    phone = models.CharField(max_length=30, verbose_name='телефон')
    city = models.CharField(max_length=30, verbose_name='город')

    username = None
    email = models.EmailField(unique=True, verbose_name='почта')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

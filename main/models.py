from django.db import models

import users.models
from users.models import User


class Course(models.Model):
    """Курс"""
    title = models.CharField(max_length=100, verbose_name='название')
    description = models.TextField(verbose_name='описание')
    preview = models.ImageField(upload_to='courses/', null=True, blank=True, verbose_name='изображение')
    created_by = models.ForeignKey('users.User', on_delete=models.CASCADE, null=True, blank=True, verbose_name='автор')

    def __str__(self):
        return f'Курс {self.title}'

    class Meta:
        verbose_name = 'курс'
        verbose_name_plural = 'курсы'


class Lesson(models.Model):
    """Урок"""
    title = models.CharField(max_length=100, verbose_name='название')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name='курс')
    description = models.TextField(verbose_name='описание')
    preview = models.ImageField(upload_to='lessons/', null=True, blank=True, verbose_name='изображение')
    link = models.URLField(verbose_name='ссылка на видео-урок')
    created_by = models.ForeignKey('users.User', on_delete=models.CASCADE, null=True, blank=True, verbose_name='автор')

    def __str__(self):
        return f'Урок {self.title} из курса:{self.course}'

    class Meta:
        verbose_name = 'урок'
        verbose_name_plural = 'уроки'


class Payment(models.Model):
    """Платеж"""

    #  варианты способа оплаты
    METHOD_CHOICES = (
        ('CASH', 'Наличные'),
        ('TRANSFER', 'Перевод на счет'),
    )

    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, verbose_name='пользователь')
    date = models.DateTimeField(verbose_name='дата оплаты')
    course = models.ForeignKey(Course, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='оплаченный курс')
    lesson = models.ForeignKey(Lesson, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='оплаченный урок')
    amount = models.PositiveIntegerField(verbose_name='сумма оплаты')
    method = models.CharField(max_length=25, choices=METHOD_CHOICES, verbose_name='способ оплаты')

    def __str__(self):
        return f'Платеж от {self.user} на сумму {self.amount}'

    class Meta:
        verbose_name = 'платеж'
        verbose_name_plural = 'платежи'

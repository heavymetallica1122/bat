from django.db import models
from django.contrib.auth.models import User


class RecyclableType(models.Model):
    """Типы материалов для переработки"""
    name = models.CharField(max_length=100, verbose_name='Название', unique=True)
    unit = models.CharField(max_length=50, verbose_name='Единица измерения', default='шт.')
    icon = models.CharField(max_length=10, verbose_name='Иконка (emoji)', default='♻️', blank=True)
    description = models.TextField(verbose_name='Описание', blank=True)
    is_active = models.BooleanField(default=True, verbose_name='Активен')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Создано')
    
    class Meta:
        verbose_name = 'Тип материала'
        verbose_name_plural = 'Типы материалов'
        ordering = ['name']
    
    def __str__(self):
        return f'{self.icon} {self.name}'


class BatterySubmission(models.Model):
    """Модель для учета сдачи вторсырья пользователями"""
    CITY_CHOICES = [
        ('moscow', 'Москва'),
        ('spb', 'Санкт-Петербург'),
        ('kazan', 'Казань'),
        ('ekb', 'Екатеринбург'),
        ('nnovgorod', 'Нижний Новгород'),
        ('samara', 'Самара'),
        ('omsk', 'Омск'),
        ('chelyabinsk', 'Челябинск'),
        ('rostov', 'Ростов-на-Дону'),
        ('ufa', 'Уфа'),
        ('krasnoyarsk', 'Красноярск'),
        ('voronezh', 'Воронеж'),
        ('perm', 'Пермь'),
        ('volgograd', 'Волгоград'),
        ('other', 'Другой'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    recyclable_type = models.ForeignKey(RecyclableType, on_delete=models.CASCADE, verbose_name='Тип материала')
    quantity = models.PositiveIntegerField(verbose_name='Количество')
    city = models.CharField(max_length=50, choices=CITY_CHOICES, verbose_name='Город', default='moscow')
    date_submitted = models.DateTimeField(auto_now_add=True, verbose_name='Дата сдачи')
    comment = models.TextField(blank=True, null=True, verbose_name='Комментарий')

    class Meta:
        verbose_name = 'Сдача вторсырья'
        verbose_name_plural = 'Сдачи вторсырья'
        ordering = ['-date_submitted']

    def __str__(self):
        return f'{self.user.username} - {self.recyclable_type.name} {self.quantity} {self.recyclable_type.unit} - {self.get_city_display()} ({self.date_submitted.strftime("%d.%m.%Y")})'

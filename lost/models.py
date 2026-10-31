from django.conf import settings
from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Категории'

class City(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Города'

class Item(models.Model):
    TYPES = [('lost', 'Потеряно'), ('found', 'Найдено')]
    STATUS = [('active', 'Активно'), ('closed', 'Закрыто')]
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='items')
    title = models.CharField(max_length=150)
    description = models.TextField()
    image = models.ImageField(upload_to='items/', blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    city = models.ForeignKey(City, on_delete=models.PROTECT)
    location = models.CharField(max_length=200, verbose_name='Место')
    event_date = models.DateField(verbose_name='Дата потери/находки')
    kind = models.CharField(max_length=10, choices=TYPES, default='lost')
    status = models.CharField(max_length=10, choices=STATUS, default='active')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Response(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='responses')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    message = models.TextField()
    phone = models.CharField(max_length=30)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [models.UniqueConstraint(fields=['item', 'user'], name='one_response_per_user_item')]

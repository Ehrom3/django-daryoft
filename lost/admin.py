from django.contrib import admin
from .models import Category, City, Item, Response
admin.site.register(Category)
admin.site.register(City)

@admin.register(Item)


class ItemAdmin(admin.ModelAdmin):
    list_display = ['title', 'kind', 'city', 'author', 'status']
    list_filter = ['kind', 'status', 'city', 'category']
admin.site.register(Response)

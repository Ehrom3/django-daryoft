from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from .models import Item, Category, City, Response
from .forms import ItemForm, ResponseForm

def home(request):
    items = Item.objects.select_related('category', 'city', 'author').order_by('-created_at')
    q = request.GET.get('q', '').strip()
    city = request.GET.get('city', '')
    category = request.GET.get('category', '')
    kind = request.GET.get('kind', '')
    if q:
        items = items.filter(Q(title__icontains=q) | Q(description__icontains=q))
    if city:
        items = items.filter(city_id=city)
    if category:
        items = items.filter(category_id=category)
    if kind in ('lost', 'found'):
        items = items.filter(kind=kind)
    return render(request, 'lost/home.html', {'items': items, 'cities': City.objects.all(), 'categories': Category.objects.all()})

def detail(request, pk):
    item = get_object_or_404(Item.objects.select_related('author', 'city', 'category'), pk=pk)
    responses = item.responses.select_related('user').all() if request.user.is_authenticated and (request.user == item.author or request.user.is_staff) else None
    return render(request, 'lost/detail.html', {'item': item, 'responses': responses})


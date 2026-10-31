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

@login_required
def create(request):
    form = ItemForm(request.POST or None, request.FILES or None)
    if request.method == 'POST' and form.is_valid():
        item = form.save(commit=False)
        item.author = request.user
        item.save()
        return redirect('detail', pk=item.pk)
    return render(request, 'lost/form.html', {'form': form, 'title': 'Новое объявление'})

@login_required
def update(request, pk):
    item = get_object_or_404(Item, pk=pk)
    if item.author != request.user and (not request.user.is_staff):
        raise PermissionDenied
    form = ItemForm(request.POST or None, request.FILES or None, instance=item)
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('detail', pk=item.pk)
    return render(request, 'lost/form.html', {'form': form, 'title': 'Изменить объявление'})

@login_required
def delete(request, pk):
    if request.method != 'POST':
        return redirect('detail', pk=pk)
    item = get_object_or_404(Item, pk=pk)
    if item.author != request.user and (not request.user.is_staff):
        raise PermissionDenied
    item.delete()
    return redirect('home')

@login_required
def respond(request, pk):
    item = get_object_or_404(Item, pk=pk)
    if item.author == request.user:
        raise PermissionDenied('Нельзя откликаться на своё объявление')
    if Response.objects.filter(item=item, user=request.user).exists():
        messages.info(request, 'Вы уже откликались на это объявление')
        return redirect('detail', pk=pk)
    form = ResponseForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        response = form.save(commit=False)
        response.item = item
        response.user = request.user
        response.save()
        messages.success(request, 'Отклик отправлен')
        return redirect('detail', pk=pk)
    return render(request, 'lost/form.html', {'form': form, 'title': 'Откликнуться'})

@login_required
def my_items(request):
    return render(request, 'lost/home.html', {'items': Item.objects.filter(author=request.user).select_related('category', 'city').order_by('-created_at'), 'mine': True})

@login_required
def my_responses(request):
    responses = Response.objects.filter(user=request.user).select_related('item').order_by('-created_at')
    return render(request, 'lost/responses.html', {'responses': responses})

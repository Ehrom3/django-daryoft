import secrets
from datetime import timedelta
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.utils import timezone
from .forms import RegisterForm, LoginForm, CodeForm, EmailForm, NewPasswordForm, ChangePasswordForm
from .models import User, EmailCode


def register(request):
    form = RegisterForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        user = form.save(commit=False)
        user.is_active = False
        user.save()
        send_code(user, 'register')
        request.session['verify_user'] = user.pk
        return redirect('verify')
    return render(request, 'accounts/form.html', {'form': form, 'title': 'Регистрация'})

def send_code(user, purpose):
    code = f'{secrets.randbelow(1000000):06d}'
    EmailCode.objects.filter(user=user, purpose=purpose).delete()
    EmailCode.objects.create(user=user, code=code, purpose=purpose)
    send_mail('Код Daryoft', f'Ваш код подтверждения: {code}', None, [user.email])
    
    
def verify(request):
    user = User.objects.filter(pk=request.session.get('verify_user'), is_active=False).first()
    if not user:
        return redirect('register')
    form = CodeForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        record = EmailCode.objects.filter(user=user, purpose='register', code=form.cleaned_data['code'], created_at__gte=timezone.now() - timedelta(minutes=10)).first()
        if record:
            user.is_active = True
            user.save()
            EmailCode.objects.filter(user=user, purpose='register').delete()
            request.session.pop('verify_user', None)
            messages.success(request, 'Почта подтверждена. Войдите.')
            return redirect('login')
        form.add_error('code', 'Неверный или просроченный код')
    return render(request, 'accounts/form.html', {'form': form, 'title': 'Подтверждение почты', 'resend': True})

def resend(request):
    if request.method != 'POST':
        return redirect('verify')
    user = User.objects.filter(pk=request.session.get('verify_user'), is_active=False).first()
    if user:
        record = EmailCode.objects.filter(user=user, purpose='register').order_by('-created_at').first()
        if record and record.created_at > timezone.now() - timedelta(seconds=60):
            messages.error(request, 'Повторная отправка доступна через 60 секунд')
        else:
            send_code(user, 'register')
            messages.success(request, 'Новый код отправлен')
    return redirect('verify')

def login_view(request):
    form = LoginForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        user = authenticate(request, username=form.cleaned_data['email'], password=form.cleaned_data['password'])
        if user:
            login(request, user)
            return redirect('home')
        form.add_error(None, 'Неверный email или пароль либо почта не подтверждена')
    return render(request, 'accounts/form.html', {'form': form, 'title': 'Вход'})

def logout_view(request):
    if request.method != 'POST':
        return redirect('home')
    logout(request)
    return redirect('home')


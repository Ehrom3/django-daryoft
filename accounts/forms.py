from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User

class RegisterForm(UserCreationForm):

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.help_text = ''
        self.fields['username'].label = 'Имя пользователя'
        self.fields['password1'].label = 'Пароль'
        self.fields['password2'].label = 'Повторите пароль'

class LoginForm(forms.Form):
    email = forms.EmailField(label='Email')
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput)

class CodeForm(forms.Form):
    code = forms.CharField(label='Шестизначный код', min_length=6, max_length=6)

class EmailForm(forms.Form):
    email = forms.EmailField(label='Email')

class NewPasswordForm(forms.Form):
    password = forms.CharField(label='Новый пароль', widget=forms.PasswordInput)

class ChangePasswordForm(forms.Form):
    old_password = forms.CharField(label='Старый пароль', widget=forms.PasswordInput)
    new_password = forms.CharField(label='Новый пароль', widget=forms.PasswordInput)

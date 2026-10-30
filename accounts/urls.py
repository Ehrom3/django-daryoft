from django.urls import path
from . import views
urlpatterns = [
    path('register/', views.register, name='register'), 
    path('verify/', views.verify, name='verify'), 
    path('resend/', views.resend, name='resend'), 
    path('login/', views.login_view, name='login'), 
    path('logout/', views.logout_view, name='logout'), 
]

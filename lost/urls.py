from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'), 
    path('item/<int:pk>/', views.detail, name='detail'), 
]

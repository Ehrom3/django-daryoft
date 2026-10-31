from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'), 
    path('item/<int:pk>/', views.detail, name='detail'), 
    path('item/new/', views.create, name='create'), 
    path('item/<int:pk>/edit/', views.update, name='update'), 
    path('item/<int:pk>/delete/', views.delete, name='delete'), 
    path('item/<int:pk>/respond/', views.respond, name='respond'),
    path('my-items/', views.my_items, name='my_items'), 
    path('my-responses/', views.my_responses, name='my_responses')
]

from django.urls import path
from . import views

urlpatterns = [
    path('', views.inventory_list, name='inventory_list'),
    path('item/<int:pk>/', views.inventory_detail, name='inventory_detail'),
    path('item/add/', views.inventory_create, name='inventory_create'),
    path('item/delete/<int:pk>/', views.inventory_delete, name='inventory_delete'),
]

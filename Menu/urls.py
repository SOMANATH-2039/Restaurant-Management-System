from django.urls import path,include
from . import views
urlpatterns = [
    path('menuitems/',views.menu,name='menu'),
    path('menuitems/<str:category>/', views.menu, name='menu_category'),
    path('product/<int:pk>',views.product,name="product"),
]

from django.urls import path
from . import views

urlpatterns = [
    path('cart/', views.cart_detail, name='cart_detail'),
    path('cart/add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/update/<int:cart_item_id>/', views.update_cart, name='update_cart'),
    path('cart/remove/<int:cart_item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('order/<int:order_id>/', views.order_detail, name='order_detail'),
    path('orders/', views.customer_orders, name='customer_orders'),
    path('cancel/<int:order_id>/',views.cancel_order,name='cancel_order'),
    path('order_list/', views.order_list, name='order_list'),
    path('orders/<int:order_id>/update-status/', views.update_order_status, name='update_order_status'),
    path('orders/<int:order_id>/cancel/', views.cancel_order, name='cancel_order'),
    path('admin_order_detail/<int:order_id>/',views.admin_order_detail,name='admin_order_detail'),
    path('orders/<int:order_id>/mark-as-paid/', views.mark_as_paid, name='mark_as_paid'),
]

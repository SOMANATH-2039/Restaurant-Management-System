from django.urls import path
from . import views
urlpatterns = [
    path('',views.home,name='home'),
    path('order/',views.order,name='order'),
    path('about/',views.about,name='about'),
    path('book_table/',views.book_table,name='book_table'),
    path('contact/',views.contact,name='contact'),
    path('search/',views.search,name="search"),
]
from django.urls import path
from . import views

urlpatterns = [
    path('register/',views.register,name='register'),
    path('login_user/',views.login_user,name='login_user'),
    path('logout/',views.logout_user,name="logout"),
    path('update_profile/',views.update_profile, name='update_profile'),
    path('dashboard/',views.admin_dashboard, name='dashboard'),
]

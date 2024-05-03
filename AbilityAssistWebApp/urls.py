from django.urls import path, include
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.user_login, name='login'),
    path('register/', views.register, name='register'),
    path('index/', views.index, name='index'),
    path('reset_password/', views.reset_password, name='reset_password'),
    path('admin_login/', views.admin_login, name='admin_login'),
    path('trips/', views.trips, name='trips'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('logout/', views.user_logout, name='logout'),
    path('edit_profile/', views.edit_profile, name='edit_profile'),




]

from django.urls import path, include
from . import views
from django.contrib import admin

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
    path('help/', views.help, name='help'),
    path('store_trip/', views.store_trip, name='store_trip'),
    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('admin/', admin.site.urls),



]

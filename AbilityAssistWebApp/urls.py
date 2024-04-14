from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('edit_profile/', views.edit_profile, name='edit_profile'),
    path('logout/', views.user_logout, name='logout'),
    path('travel_history/', views.travel_history, name='travel_history'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('saved_locations/', views.saved_locations, name='saved_locations'),


]

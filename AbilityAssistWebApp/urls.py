from django.urls import path, include
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('reset_password/login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('volunteer_login/', views.volunteer_login, name='volunteer_login'),
    path('volunteer_register/', views.volunteer_register, name='volunteer_register'),
    path('edit_profile/', views.edit_profile, name='edit_profile'),
    path('travel_history/', views.travel_history, name='travel_history'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('saved_locations/', views.saved_locations, name='saved_locations'),
    path('logout/', views.user_logout, name='logout'),  # Use custom logout view here
    path('reset_password/', include('django.contrib.auth.urls')),



]

from django.urls import path, include
from . import views
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls import static


urlpatterns = [
    path('', views.user_login, name='login'),
    path('register/', views.register, name='register'),
    path('index/', views.index, name='index'),
    path('trips/', views.trips, name='trips'),
    path('trips_pdf/', views.trips_pdf, name='trips_pdf'),
    path('index/store_trip/', views.store_trip, name='store_trip'),
    path('update_final_destination/<int:trip_id>/', views.update_final_destination, name='update_final_destination'),
    path('cancel_trip/<int:trip_id>/', views.cancel_trip, name='cancel_trip'),
    path('recent_trip/', views.recent_trip, name='recent_trip'),
    path('user_stats/', views.user_stats, name='user_stats'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('logout/', views.user_logout, name='logout'),
    path('edit_profile/', views.edit_profile, name='edit_profile'),
    path('help/', views.help, name='help'),
    path('admin/', admin.site.urls),
    path('deactivate/', views.deactivate_user, name='deactivate_user'),
    path('reset_password/', auth_views.PasswordResetView.as_view(template_name="reset_password.html"), name="reset_password"),
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(template_name="password_reset_done.html"), name="password_reset_done"),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name="password_reset_confirm.html"), name="password_reset_confirm"),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(template_name="password_reset_complete.html"), name="password_reset_complete"),

]

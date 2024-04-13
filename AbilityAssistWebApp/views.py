from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import CustomUser, TravelHistory
from .serializers import UserRegistrationSerializer, UserLoginSerializer
from django.contrib import messages
from django.core.mail import send_mail
from django.urls import reverse


def index(request):
    return render(request, 'index.html')


def register(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        username = request.POST.get('username')
        last_name = request.POST.get('last_name')
        phone = request.POST.get('phone')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        # You can add your own validation logic here before saving the user

        # Create a dictionary with the form data
        data = {
            'email': email,
            'username': username,
            'last_name': last_name,
            'phone': phone,
            'password': password,
            'confirm_password': confirm_password
        }

        # Serialize the data and validate it
        serializer = UserRegistrationSerializer(data=data)
        if serializer.is_valid():
            # Save the user
            user = serializer.save()

            # Log in the user after registration
            user = authenticate(email=email, password=password)
            if user:
                login(request, user)

            return redirect('index')
    else:
        # Initialize an empty serializer for GET requests
        serializer = UserRegistrationSerializer()

    return render(request, 'register.html', {'form': serializer})


def user_login(request):
    template_name = 'login.html'
    error = None  # Define the error variable at the beginning

    if request.method == 'POST':
        serializer = UserLoginSerializer(data=request.POST)
        if serializer.is_valid():
            user = authenticate(email=serializer.validated_data['email'],
                                password=serializer.validated_data['password'])
            if user:
                login(request, user)
                return redirect('index')
            else:
                error = 'Invalid email or password'
        else:
            errors = serializer.errors
    else:
        errors = None
        serializer = UserLoginSerializer()  # Initialize an empty serializer for GET requests

    return render(request, template_name, {'form': serializer, 'error': error, 'errors': errors})


@login_required
def edit_profile(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')

        # Update user_profile with new data
        user_profile = request.user
        user_profile.first_name = first_name
        user_profile.last_name = last_name
        user_profile.email = email
        user_profile.save()

        messages.success(request, 'Your profile has been updated successfully.')
        return redirect('index')

    else:
        messages.error(request, 'Your profile update experienced an error.')

    return render(request, 'edit_profile.html')


@login_required
def user_logout(request):
    logout(request)
    return redirect('index')


def travel_history(request):
    travel_entries = TravelHistory.objects.filter(logged_user=request.user)
    return render(request, 'travel_history.html', {'travel_entries': travel_entries})


def about(request):
    return render(request, 'about.html')


def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')

        if not name or not email or not message:
            messages.error(request, 'Please fill in all fields.')
            return redirect('contact')

        send_mail(
            'New message from AbilityAssist contact form',
            f'Name: {name}\nEmail: {email}\nMessage: {message}',
            'abilityassistcompany@gmail.com',
            ['abilityassistcompany@gmail.com'],
            fail_silently=False,
        )

        messages.success(request, 'Your message has been sent successfully.')
        return redirect(reverse('contact'))

    return render(request, 'contact.html')


def saved_locations(request):
    return render(request, 'saved_locations.html')


def user_list(request):
    users = CustomUser.objects.all()
    return render(request, 'user_list.html', {'users': users})

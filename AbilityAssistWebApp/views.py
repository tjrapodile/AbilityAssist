from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout as auth_logout
from .models import UserProfile, TravelHistory
from .forms import RegistrationForm, LoginForm
from django.contrib import messages
from django.core.mail import send_mail
from django.urls import reverse
def index(request):
    return render(request, 'index.html')


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Save UserProfile
            UserProfile.objects.create(
                user=user,
                phone=form.cleaned_data['phone']
            )
            messages.success(request, 'Account created successfully. You can now log in.')
            return redirect('login')  # Redirect to login page after successful registration
        else:
            # Form is invalid, display errors
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field.capitalize()}: {error}')
    else:
        form = RegistrationForm()
    return render(request, 'register.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request, username=email, password=password)
            if user is not None:
                login(request, user)
                return redirect('index')  # Assuming 'index' is a valid URL pattern name
            else:
                messages.error(request, 'Invalid email or password. Please try again.')
        else:
            messages.error(request, 'Invalid form submission. Please check your input.')
    else:
        form = LoginForm()

    return render(request, 'login.html', {'form': form})

@login_required
def edit_profile(request):
    user_profile = UserProfile.objects.get(email=request.user.email)

    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')

        # Update user_profile with new data
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
    auth_logout(request)
    return redirect('index')


def travel_history(request):
    travel_entries = TravelHistory.objects.filter(user=request.user)
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

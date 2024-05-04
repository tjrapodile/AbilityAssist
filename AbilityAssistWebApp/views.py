from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from .forms import RegistrationForm, LoginForm, EditUserForm
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
            user.save()
            profile = authenticate(request, username=user.username, password=user.password)
            login(request, user)
            return redirect('index')  # Replace 'index' with the name of the URL pattern for your desired page
    else:
        form = RegistrationForm()

    return render(request, 'register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('index')
            else:
                # Invalid credentials, display error message
                return render(request, 'login.html', {'form': form, 'error_message': 'Invalid username or password. Please try again.'})
        else:
            # Invalid form submission, display error message
            return render(request, 'login.html', {'form': form, 'error_message': 'Invalid form submission. Please check your input.'})
    else:
        form = LoginForm()
        return render(request, 'login.html', {'form': form})



@login_required
def user_logout(request):
    logout(request)
    return redirect('login')

@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = EditUserForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save(request=request,user=request.user)
            return redirect('index')  # Redirect to the user's profile page after editing
    else:
        form = EditUserForm(instance=request.user)
    return render(request, 'edit_profile.html', {'form': form})


def trips(request):
    return render(request, 'trips.html')

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


def admin_login(request):
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

    return render(request, 'admin_login.html', {'form': form})



@login_required
def reset_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Password changed successfully!')
            return redirect('profile')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'change_password.html', {'form': form})




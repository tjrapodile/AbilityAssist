from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from .models import Users, TravelHistory
from .forms import RegistrationForm, LoginForm, PasswordResetForm, UserProfileForm
from django.contrib import messages
from django.core.mail import send_mail
from django.urls import reverse
from django.contrib.auth.models import User
def index(request):
    return render(request, 'index.html')


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            # Extract data from the form
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            phone = form.cleaned_data['phone']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password1']

            # Create the user
            user = User.objects.create_user(username=email, email=email, password=password, first_name=first_name,last_name=last_name)

            # Create the user profile
            Users.objects.create(user=user, phone=phone)

            # Authenticate and login the user
            user = authenticate(request, username=email, password=password)
            login(request, user)

            # Redirect to a success page or any other desired page
            return redirect('index')  # Replace 'index' with the name of the URL pattern for your desired page
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
                return redirect('index')
            else:
                messages.error(request, 'Invalid email or password. Please try again.')
        else:
            messages.error(request, 'Invalid form submission. Please check your input.')
    else:
        form = LoginForm()

    return render(request, 'login.html', {'form': form})

@login_required
def edit_profile(request):
    user_profile = Users.objects.get(user=request.user)

    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=user_profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been updated successfully.')
            return redirect('index')
        else:
            messages.error(request, 'Your profile update experienced an error.')
    else:
        form = UserProfileForm(instance=user_profile)

    return render(request, 'edit_profile.html', {'form': form})


@login_required
def user_logout(request):
    logout(request)
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


def volunteer_register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            # Save the user
            form.save()

            # Authenticate and login the user
            user = authenticate(request, username=form.cleaned_data['email'], password=form.cleaned_data['password1'])
            login(request, user)

            # Redirect to a success page or any other desired page
            return redirect('index')  # Replace 'index' with the name of the URL pattern for your desired page
    else:
        form = RegistrationForm()

    return render(request, 'volunteer_register.html', {'form': form})

def volunteer_login(request):
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

    return render(request, 'volunteer_login.html', {'form': form})



def reset_password(request):
    if request.method == 'POST':
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            # Check if the email exists in the database
            if Users.objects.filter(email=email).exists():
                # Generate and send the reset link
                reset_link = request.build_absolute_uri(reverse('password_reset_confirm'))
                send_mail(
                    'Password Reset',
                    f'Click the link below to reset your password:\n{reset_link}',
                    'from@example.com',  # Replace with your email address
                    [email],
                    fail_silently=False,
                )
                messages.success(request, 'Password reset link sent to your email.')
                return redirect('login')  # Assuming 'login' is the name of the login page URL
            else:
                messages.error(request, 'Email address not found.')
        else:
            messages.error(request, 'Invalid form submission. Please check your input.')
    else:
        form = PasswordResetForm()
    return render(request, 'reset_password.html', {'form': form})




import json

from django.contrib.auth.forms import PasswordChangeForm, AuthenticationForm
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.views.decorators.csrf import csrf_exempt

from .forms import RegistrationForm, LoginForm, EditUserForm
from django.contrib import messages
from django.core.mail import send_mail
from django.urls import reverse
from django.http import JsonResponse

from .models import Trip,InitialGeolocation, FinalGeolocation


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
                if user.is_staff:
                    login(request,user)
                    return redirect(reverse('admin:index'))
                login(request, user)
                return redirect('index')
            else:
                # Invalid credentials, display error message
                messages.error(request, 'Invalid username or password. Please try again. (If you have deactivated your account, please contact <a href="mailto:Abilityassistcompany@gmail.com">Abilityassistcompany@gmail.com</a> if you wish to re-activate it)')
                return render(request, 'login.html', {'form': form})
        else:
            # Invalid form submission, display error message
            messages.error(request, 'Invalid form submission. Please check your input.')
            return render(request, 'login.html', {'form': form})
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

@login_required
def deactivate_user(request):
    if request.method == "POST":
        user = request.user
        user.is_active = False  # Mark the user as inactive
        user.save()
        user_logout(request)
        # Redirect the user to the login page
        return redirect('login')
    else:
        return JsonResponse({"error": "Invalid request method"}, status=400)
@csrf_exempt
def store_trip(request):
    if request.method == "POST":
        # Extract data from POST request
        initial_point_latitude = request.POST.get('initialPoint[latitude]')
        initial_point_longitude = request.POST.get('initialPoint[longitude]')
        final_destination_value = request.POST.get('finalPoint[finalDestinationValue]')
        final_destination_name = request.POST.get('finalPoint[finalDestinationName]')

        # Create new InitialGeolocation instance for start_point
        start_point_instance = InitialGeolocation.objects.create(
            latitude=initial_point_latitude,
            longitude=initial_point_longitude
        )

        # Find or create FinalGeolocation instance for destination
        end_point_instance, created = FinalGeolocation.objects.get_or_create(
            value=final_destination_value,
            name=final_destination_name
        )

        # Create new Trip object and save it to the database
        trip = Trip.objects.create(
            user=request.user,  # Assuming user is authenticated
            start_point=start_point_instance,
            end_point=end_point_instance
        )

        # Redirect the user back to the index page after successfully storing the trip
        return redirect('index')
    else:
        # Return error response if request method is not POST
        return JsonResponse({'error': 'Invalid request method'}, status=400)



@login_required
def trips(request):
    if request.method == 'GET':
        # Filter trips based on the logged-in user
        travel_entries = Trip.objects.filter(user=request.user)
        return render(request, 'trips.html', {'travel_entries': travel_entries})
    else:
        return JsonResponse({'error': 'Only GET requests are allowed for displaying trip data'}, status=405)


def about(request):
    return render(request, 'about.html')

def contact(request):
    if request.method == 'POST':
        pass
    return render(request, 'contact.html')


def help(request):
    return render(request,'help.html')






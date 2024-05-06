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

def store_trip(request):
    if request.method == "POST":
        # Extract data from POST request
        start_point = request.POST.get('start_point')
        destination = request.POST.get('destination')

        # Create new Trip object and save it to the database
        trip = Trip.objects.create(
            user=request.user,  # Assuming user is authenticated
            start_point=start_point,
            destination=destination
        )

        # Return success response
        return JsonResponse({'message': 'Trip stored successfully!'})
    else:
        # Return error response if request method is not POST
        return JsonResponse({'error': 'Invalid request method'}, status=400)


@csrf_exempt  # Disable CSRF protection for this view for simplicity (use proper CSRF protection in production)
def trips(request):
    print("executing trips in view")
    if request.method == 'POST':
        try:
            # Parse JSON data from request body
            json_data = json.loads(request.body)
            print("here is the data from front end: " + json_data['finalPoint']['finalDestinationName'])

            # Extract data from JSON and save it to the database

            initialData = InitialGeolocation(
                longitude=json_data['initialPoint']['longiTude'],
                latitude=json_data['initialPoint']['latitude']
            )
            initialData.save()

            finalData = FinalGeolocation(
                value=json_data['finalPoint']['finalDestinationValue'],
                destination_name=json_data['finalPoint']['finalDestinationName']
            )
            finalData.save()

            trip = Trip(
                start_point=initialData,
                end_point=finalData
            )
            trip.save()

            return JsonResponse({'message': 'Data saved successfully'}, status=201)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON format in request body'}, status=400)
        except KeyError as e:
            return JsonResponse({'error': f'Missing key in JSON data: {e}'}, status=400)
    elif request.method == 'GET':
        travel_entries = Trip.objects.all()
        return render(request, 'trips.html', {'travel_entries': travel_entries})
    else:
        return JsonResponse({'error': 'Only GET and POST requests are allowed'}, status=405)



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
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None and user.is_superuser:
                print("User is a superuser.")
                login(request, user)
                return redirect('admin_dashboard')
            else:
                messages.error(request, 'Invalid username or password. Please try again.')
        else:
            messages.error(request, 'Invalid form submission. Please check your input.')
    else:
        form = AuthenticationForm(request)

    return render(request, 'admin_login.html', {'form': form})

def admin_dashboard(request):
    if request.user.is_authenticated and request.user.is_superuser:
        return redirect('/admin/')
    else:
        return redirect('admin_login')

@login_required
def reset_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Email containing the next steps have been sent!')
            return redirect('change_password')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'change_password.html', {'form': form})

def help(request):
    return render(request,'help.html')






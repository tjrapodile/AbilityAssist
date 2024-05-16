from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
import json
from .forms import RegistrationForm, LoginForm, EditUserForm
from .models import Trip, InitialGeolocation, FinalGeolocation, AboutImage
from django.contrib.auth.models import User
from django.db.models import Q
from django.core.paginator import Paginator
from reportlab.pdfgen import canvas
from dateutil.parser import parse
from dateutil.parser import ParserError
from django.utils import timezone
from django.views.decorators.http import require_POST
from django.db.models import Count

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
@login_required
@require_POST  # Ensures that this view can only be accessed by POST requests
def store_trip(request):
    # We no longer need to explicitly check if the method is POST due to the @require_POST decorator
    data = json.loads(request.body)
    initial_point_latitude = data['initialPoint']['latitude']
    initial_point_longitude = data['initialPoint']['longitude']
    final_destination_value = data['finalPoint']['finalDestinationValue']
    final_destination_name = data['finalPoint']['finalDestinationName']

    start_point_instance = InitialGeolocation.objects.create(
        latitude=initial_point_latitude,
        longitude=initial_point_longitude
    )

    end_point_instance, created = FinalGeolocation.objects.get_or_create(
        value=final_destination_value,
        name=final_destination_name
    )

    user_instance = request.user

    trip = Trip.objects.create(
        user=user_instance,
        start_point=start_point_instance,
        end_point=end_point_instance
    )

    response = {
        'trip_id': trip.id,
        'start_point': {
            'latitude': start_point_instance.latitude,
            'longitude': start_point_instance.longitude
        },
        'end_point': {
            'value': end_point_instance.value,
            'name': end_point_instance.name
        }
    }

    return JsonResponse(response, status=201)

@login_required
def trips(request):
    search_query = request.GET.get('search', '').strip()

    if search_query:
        # Try parsing the search_query as a date
        try:
            search_date = parse(search_query, fuzzy=False)
            date_filter = Q(date__date=search_date.date())
        except ParserError:
            # If parsing fails, assume search_query is a destination name
            date_filter = Q()

        # Apply filters based on the user's query
        travel_entries = Trip.objects.filter(
            Q(user=request.user) &
            (Q(end_point__name__icontains=search_query) | date_filter)
        ).order_by('-date')
    else:
        # If no search query is provided, just list all trips for the user
        travel_entries = Trip.objects.filter(user=request.user).order_by('-date')

    # Pagination
    paginator = Paginator(travel_entries, 10)  # Show 10 trips per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'travel_entries': page_obj,
        'search_query': search_query,
    }

    return render(request, 'trips.html', context)

@login_required
def trips_pdf(request):
    # Create the HttpResponse object with the appropriate PDF headers.
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="trips.pdf"'

    # Create the PDF object, using the response object as its "file."
    p = canvas.Canvas(response)

    # Get the user's trips and add them to the PDF.
    trips = Trip.objects.filter(user=request.user).order_by('-date')

    # Start writing the PDF here using reportlab functions.
    y_pos = 800
    for trip in trips:
        p.drawString(100, y_pos,
                     f"Trip ID: {trip.id}, Destination: {trip.end_point.name}, Date: {trip.date.strftime('%Y-%m-%d %H:%M:%S')}")
        y_pos -= 20
        if y_pos < 100:
            p.showPage()
            y_pos = 800

    # Close the PDF object cleanly, and we're done.
    p.showPage()
    p.save()
    return response

@login_required
@require_POST
def update_final_destination(request, trip_id):
    data = json.loads(request.body)
    final_destination_value = data['finalDestinationValue']
    final_destination_name = data['finalDestinationName']

    end_point_instance, created = FinalGeolocation.objects.get_or_create(
        value=final_destination_value,
        name=final_destination_name
    )

    trip = Trip.objects.get(id=trip_id, user=request.user)
    trip.end_point = end_point_instance
    trip.cancelled = False
    trip.save()

    return JsonResponse({'success': 'Final destination updated successfully'}, status=200)


@login_required
@require_POST
def cancel_trip(request, trip_id):
    trip = Trip.objects.get(id=trip_id, user=request.user)
    trip.cancelled = True
    trip.save()
    # Optionally, you can log the cancellation to the Django server console
    print(f'Trip ID {trip_id} cancelled successfully.')
    return JsonResponse({'success': 'Trip cancelled successfully'}, status=200)


@login_required
def recent_trip(request):
    try:
        latest_trip = Trip.objects.filter(user=request.user).latest('date')
    except Trip.DoesNotExist:
        latest_trip = None

    if 'pdf' in request.GET and latest_trip is not None:
        # Generate PDF response
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="recent_trip_{latest_trip.id}.pdf"'
        p = canvas.Canvas(response)
        p.drawString(100, 750, f"User: {request.user.username}")
        p.drawString(100, 735, f"Trip ID: {latest_trip.id}")
        p.drawString(100, 720, f"Start Location: {latest_trip.start_point.latitude}, {latest_trip.start_point.longitude}")
        p.drawString(100, 705, f"Destination: {latest_trip.end_point.name}")
        p.drawString(100, 690, f"Date: {latest_trip.date.strftime('%Y-%m-%d %H:%M:%S')}")
        p.drawString(100, 675, f"Cancelled: {'Yes' if latest_trip.cancelled else 'No'}")
        p.showPage()
        p.save()
        return response
    else:
        # HTML response
        context = {'latest_trip': latest_trip}
        return render(request, 'recent_trip.html', context)


@login_required
def user_stats(request):
    search_query = request.GET.get('search', None)
    user_stats_list = User.objects.annotate(trip_count=Count('trip')).order_by('-trip_count')

    if search_query:
        try:
            position = int(search_query) - 1  # Adjust for zero indexing
            user_stats = [user_stats_list[position]] if position < len(user_stats_list) else []
        except (ValueError, IndexError):
            user_stats = []
    else:
        user_stats = user_stats_list

    # Pagination
    paginator = Paginator(user_stats, 10)  # Show 10 results per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    if 'pdf' in request.GET:
        # Generate PDF response for all users, ignoring pagination and search
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="user_stats.pdf"'
        p = canvas.Canvas(response)

        title = "User Stats"
        p.drawString(200, 800, title)
        p.drawString(100, 780, "Username")
        p.drawString(400, 780, "Number of Trips")

        height = 760
        for user in user_stats_list:
            p.drawString(100, height, str(user.username))
            p.drawString(400, height, str(user.trip_count))
            height -= 20
            if height < 100:  # Check for new page
                p.showPage()
                height = 800

        p.showPage()
        p.save()
        return response
    else:
        context = {'user_stats': page_obj, 'search_query': search_query}
        return render(request, 'user_stats.html', context)

def about(request):
    aboutImage = AboutImage.objects.first()
    context = {'aboutImage': aboutImage}
    return render(request, 'about.html', context)

def contact(request):
    if request.method == 'POST':
        pass
    return render(request, 'contact.html')


def help(request):
    return render(request,'help.html')






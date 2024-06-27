from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.middleware.csrf import get_token
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import re
import json
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.middleware.csrf import get_token
from django.views.decorators.csrf import csrf_exempt
import json
import re
from .models import Appointment
from datetime import datetime, timedelta, time


def get_csrf_token(request):
    return JsonResponse({'csrfToken': get_token(request)})

@csrf_exempt
def home(request):
    return JsonResponse({'message': 'Welcome to the home page'})


@csrf_exempt
def signup(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)

        username = data.get('username')
        fname = data.get('fname', '')  # Handle optional field with default value
        lname = data.get('lname', '')  # Handle optional field with default value
        email = data.get('email')
        pass1 = data.get('pass1')
        pass2 = data.get('pass2')

        print(request.POST.get('username'))
        # Basic validations
        if not (username and email and pass1 and pass2):
            return JsonResponse({'error': 'All fields are required'}, status=400)

        if User.objects.filter(username=username).exists():
            return JsonResponse({'error': 'Username already exists! Please try another username'}, status=400)

        if User.objects.filter(email=email).exists():
            return JsonResponse({'error': 'Email already registered!'}, status=400)

        if pass1 != pass2:
            return JsonResponse({'error': 'Passwords did not match'}, status=400)

        if len(username) > 10:
            return JsonResponse({'error': 'Username must be under 10 characters'}, status=400)

        if not username.isalnum():
            return JsonResponse({'error': 'Username must be alpha-numeric!'}, status=400)

        # Additional email format validation
        if not re.match(r'^[\w\.-]+@[\w\.-]+$', email):
            return JsonResponse({'error': 'Invalid email format'}, status=400)

        # Create user and save
        myuser = User.objects.create_user(username, email, pass1)
        myuser.first_name = fname
        myuser.last_name = lname
        myuser.save()

        return JsonResponse({'message': 'Your account has been successfully created'}, status=201)

    return JsonResponse({'error': 'Invalid request method'}, status=400)

@csrf_exempt
def signin(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)

        username = data.get('username')
        pass1 = data.get('pass1', '') 

        user = authenticate(username=username, password=pass1)

        if user is not None:
            login(request, user)
            return JsonResponse({'message': 'Logged in successfully', 'user': {
                'username': user.username,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'email': user.email,
            }})
        else:
            return JsonResponse({'error': 'Invalid credentials. Please sign up if you do not have an account.'}, status=400)

    return JsonResponse({'error': 'Invalid request method'}, status=400)

@csrf_exempt
def signout(request):
    logout(request)
    return JsonResponse({'message': 'Logged out successfully'})



@csrf_exempt
def book_appointment(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)

        username = data.get('username')
        name = data.get('name')
        contact_number = data.get('contact_number')
        email = data.get('email')
        service_required = data.get('service_required')
        appointment_date = data.get('appointment_date')
        appointment_time = data.get('appointment_time')

        if not (username and name and contact_number and email and service_required and appointment_date and appointment_time):
            return JsonResponse({'error': 'All fields are required'}, status=400)

        user = User.objects.filter(username=username).first()
        if not user:
            return JsonResponse({'error': 'User does not exist, Please try with an existing username'}, status=400)

        # Save appointment
        appointment = Appointment.objects.create(
            user=user,
            name=name,
            contact_number=contact_number,
            email=email,
            service_required=service_required,
            appointment_date=appointment_date,
            appointment_time=appointment_time
        )
        appointment.save()

        return JsonResponse({'message': 'Appointment booked successfully'}, status=201)

    return JsonResponse({'error': 'Invalid request method'}, status=400)


@csrf_exempt
def get_user_appointments(request, username):
    user = User.objects.filter(username=username).first()
    if not user:
        return JsonResponse({'error': 'User does not exist'}, status=400)

    appointments = Appointment.objects.filter(user=user)
    appointments_data = [{
        'name': appointment.name,
        'contact_number': appointment.contact_number,
        'email': appointment.email,
        'service_required': appointment.service_required,
        'appointment_date': appointment.appointment_date,
        'appointment_time': appointment.appointment_time
    } for appointment in appointments]

    return JsonResponse({'appointments': appointments_data})



def generate_time_slots(start_time, end_time, slot_duration_minutes):
    slots = []
    current_time = start_time
    while current_time < end_time:
        slots.append(current_time.strftime('%H:%M'))
        current_time = (datetime.combine(datetime.today(), current_time) + timedelta(minutes=slot_duration_minutes)).time()
    return slots


@csrf_exempt
def get_available_slots(request):
    if request.method == "GET":
        try:
            date_str = request.GET.get('date')
            date = datetime.strptime(date_str, '%Y-%m-%d').date() if date_str else datetime.today().date()
        except ValueError:
            return JsonResponse({'error': 'Invalid date format, Please input YYYY-MM-DD'}, status=400)

        start_time = time(9, 0)  # Start of the working day
        end_time = time(17, 0)   # End of the working day
        slot_duration_minutes = 30  # Slot duration in minutes

        available_dates = [(date + timedelta(days=i)).strftime('%Y-%m-%d') for i in range(-2, 3)]
        available_slots = {}

        for available_date in available_dates:
            date_obj = datetime.strptime(available_date, '%Y-%m-%d').date()
            all_slots = generate_time_slots(start_time, end_time, slot_duration_minutes)
            booked_slots = Appointment.objects.filter(appointment_date=date_obj).values_list('appointment_time', flat=True)
            booked_slots = [time.strftime('%H:%M') for time in booked_slots]
            available_slots[available_date] = [slot for slot in all_slots if slot not in booked_slots]

        return JsonResponse({'available_slots': available_slots}, status=200)

    return JsonResponse({'error': 'Invalid request method'}, status=400)

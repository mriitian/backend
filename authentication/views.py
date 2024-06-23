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

def get_csrf_token(request):
    return JsonResponse({'csrfToken': get_token(request)})

@csrf_exempt
def home(request):
    return JsonResponse({'message': 'Welcome to the home page'})


@csrf_exempt
def signup(request):
    if request.method == "POST":
        data = json.loads(request.body)
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
        data = json.loads(request.body)
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


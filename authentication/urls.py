from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('csrf_token/', views.get_csrf_token, name='csrf_token'),
    path('home/', views.home, name='home'),
    path('signup/', views.signup, name='signup'),
    path('signin/', views.signin, name='signin'),
    path('signout/', views.signout, name='signout'),
    path('book_appointment', views.book_appointment, name='book_appointment'),
    path('get_user_appointments/<str:username>/', views.get_user_appointments, name='get_user_appointments'),
    path('get_available_slots/', views.get_available_slots, name='get_available_slots'),
]

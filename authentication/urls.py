from django.contrib import admin
from django.urls import path, include
from . import views
urlpatterns = [
    path('', views.home, name="home"),
    path('signup/', views.signup, name="signup"),
    path('signin/', views.signin, name="signin"),
    path('signout/', views.signout, name="signout"),
    # path('activate/<uidb64>/<token>/', views.activate, name='activate'),
    # path('get_csrf_token/', views.get_csrf_token, name='get_csrf_token'),
]

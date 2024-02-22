from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.create_registration, name="register"),
    path('login/', views.user_login, name="user_login"),
    path('get-username/', views.get_admin_username, name="get-username"),
]
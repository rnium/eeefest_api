from django.contrib import admin
from django.urls import path
from . import views

app_name = "fest_api"

urlpatterns = [
    path('register/', views.create_registration, name="register"),
    path('login/', views.user_login, name="user_login"),
    path('logout/', views.user_logout, name="user_logout"),
    path('get-username/', views.get_admin_username, name="get_username"),
    path('registrations/', views.RegistrationsList.as_view(), name="registrations_list"),
    path('approve-registration/<int:pk>/', views.approve_registration, name="approve_registration"),
    path('send-confirmation/<int:pk>/', views.send_registration_confirmation, name="send_registration_confirmation"),
    path('deleteregistration/', views.delete_registration, name="delete_registration"),
]
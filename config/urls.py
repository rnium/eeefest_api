from django.contrib import admin
from django.urls import path, include
from fest import views


urlpatterns = [
    path('django-admin/', admin.site.urls),
    path('api/', include('fest.api.urls')),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
    path('assets/<str:filename>', views.download_asset),
    path('responseexcel/', views.download_response_excel, name="download_response_excel"),
    path('entrypass/<str:reg_code>/', views.download_entrypass, name="download_entrypass"),
    path('verify-registration/<str:reg_code>/', views.verify_registration, name="verify_registration"),   
]

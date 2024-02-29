"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path, include
from django.views.generic import TemplateView
from fest import views

exclude_prefixes = ['admin']
exclude_pattern = '|'.join(exclude_prefixes)

urlpatterns = [
    path('django-admin/', admin.site.urls),
    path('api/', include('fest.api.urls')),
    path('assets/<str:filename>', views.download_asset),
    path('admin/', TemplateView.as_view(template_name='admin_site/index.html')),
    re_path(rf'^(?!({exclude_pattern})/).*$', TemplateView.as_view(template_name='main_site/index.html'))
]

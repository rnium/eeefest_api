from django.shortcuts import render
from django.http import FileResponse, HttpResponse
from django.conf import settings
import os



def download_asset(request, filename):
    filepath = settings.BASE_DIR / ('frontend/main_site/static/assets/' + filename)
    print(filepath)
    if os.path.exists(filepath):
        return FileResponse(open(filepath, 'rb'), filename=filename)
    return HttpResponse(f"File not found!")
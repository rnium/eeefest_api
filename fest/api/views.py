from rest_framework.response import Response
from rest_framework.decorators import api_view
from fest.models import Registration
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from .serializer import RegistrationSerializer


@api_view(['POST'])
@csrf_exempt
def create_registration(request):
    print(request.META.get('REMOTE_ADDR'))
    data = request.data.copy()
    data['ip_address'] = request.META.get('REMOTE_ADDR')
    serializer = RegistrationSerializer(data=data)

    if serializer.is_valid():
        serializer.save()
        return Response(data=serializer.data)
    else:
        return Response(data=serializer.errors)
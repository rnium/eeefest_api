from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from fest.models import Registration, GroupMember
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.utils import timezone
from .serializer import RegistrationSerializer
from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from .utils import check_registration_data

@api_view()
def get_admin_username(request):
    data = {'username': None}
    if request.user.is_authenticated:
        data['username'] = request.user.get_username()
    return Response(data=data)


@api_view(['POST'])
def user_login(request):
    if user:= authenticate(request, username=request.data.get('username'), password=request.data.get('password')):
        login(request, user)
        return Response(data={'info': 'ok', 'username': user.get_username()})
    else:
        return Response(data={'info': 'not ok'}, status=status.HTTP_401_UNAUTHORIZED)

@api_view()
@permission_classes([IsAuthenticated])
def user_logout(request):
    logout(request)
    return Response(data={'info': 'Logged out'})
    
class RegistrationsList(ListAPIView):
    serializer_class = RegistrationSerializer
    def get_queryset(self):
        contest = self.request.GET.get('contest', 'all')
        approval = self.request.GET.get('approval', 'all')
        registrations = None
        if contest == 'all':
            if approval == 'all':
                registrations = Registration.objects.all()
            elif approval == 'approved':
                registrations = Registration.objects.filter(is_approved=True)
            else:
                registrations = Registration.objects.filter(is_approved=False)
        else:
            if approval == 'all':
                registrations = Registration.objects.filter(contest=contest)
            elif approval == 'approved':
                registrations = Registration.objects.filter(contest=contest, is_approved=True)
            else:
                registrations = Registration.objects.filter(contest=contest, is_approved=False)
        if registrations != None:
            registrations = registrations.order_by('is_approved', '-added_at')
        return registrations
    
    
@api_view(['POST'])
def create_registration(request):
    json_data = request.data
    data = json_data.get('formData')
    data['ip_address'] = request.META.get('REMOTE_ADDR')
    members_data = json_data.get('groupFormData')
    success, info = check_registration_data(data, members_data)
    if not success:
        return Response(data={'info': info}, status=status.HTTP_400_BAD_REQUEST)
    if data['group_members_count'] == '':
        data['group_members_count'] = 1
    reg_serializer = RegistrationSerializer(data=data)
    if reg_serializer.is_valid():
        registration = reg_serializer.save()
    else:
        print(reg_serializer.errors)
        return Response(data={'info': "Cannnot register"}, status=status.HTTP_400_BAD_REQUEST)
    for member_key in members_data:
        member_data = members_data[member_key]
        member_data['registration'] = registration
        member = GroupMember(**member_data)
        member.save()
    return Response(data={'info': "Saved"})


@api_view()
@permission_classes([IsAuthenticated])
def approve_registration(request, pk):
    reg = get_object_or_404(Registration, pk=pk)
    if reg.is_approved:
        return Response(data={"info": f'Regisration: {reg.id} Already Approved!'}, status=status.HTTP_400_BAD_REQUEST)
    reg.is_approved = True
    reg.approved_by = request.user
    reg.approved_at = timezone.now()
    reg.save()
    return Response(data={"info": f'Regisration: {reg.id} Approved'})
    
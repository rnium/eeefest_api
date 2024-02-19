from rest_framework.response import Response
from rest_framework.decorators import api_view
from fest.models import Registration, GroupMember
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from .serializer import RegistrationSerializer



@csrf_exempt
@api_view(['POST'])
def create_registration(request):
    data = request.data.get('formData')
    data['ip_address'] = request.META.get('REMOTE_ADDR')
    members_data = request.data.get('groupFormData')
    if data['group_members_count'] == '':
        data['group_members_count'] = 1
    registration = Registration(**data)
    registration.save()
    for member_key in members_data:
        print(member_key)
        m_data = members_data[member_key]
        if member_key != 'others' and len(m_data.get('name', '')) == 0:
            continue
        if member_key == 'others':
            if len(m_data) > 0:
                m_data = {}
                m_data['other_info'] = members_data[member_key]
            else:
                continue
        elif member_key == 'team_leader':
            if 'reg' in m_data :
                m_data['reg_num'] = m_data['reg']
                m_data.pop('reg')
        else:
            if 'reg' in m_data:
                m_data.pop('reg')
        m_data['registration'] = registration
        member = GroupMember(**m_data)
        member.save()
    return Response(data={'info': registration.id})
        
from rest_framework import serializers
from fest.models import Registration, GroupMember
from django.urls import reverse


class RegistrationSerializer(serializers.ModelSerializer):
    team_leader = serializers.SerializerMethodField()
    approval_link = serializers.SerializerMethodField()
    confirmation_link = serializers.SerializerMethodField()
    approved_by = serializers.SerializerMethodField()
    class Meta:
        model = Registration
        fields = "__all__"
        
    def get_team_leader(self, obj):
        member_1 = obj.groupmember_set.all().first()
        if member_1:
            return {
                "name": member_1.name, 
                "inst": member_1.inst, 
            }
        else:
            return "<empty>"
    
    def get_approval_link(self, obj):
        return reverse("fest_api:approve_registration", args=(obj.id,)) 
       
    def get_confirmation_link(self, obj):
        if not obj.is_email_sent:
            return reverse("fest_api:send_registration_confirmation", args=(obj.id,))
        return ""
    
    def get_approved_by(self, obj):
        if not obj.is_approved:
            return None
        else:
            if obj.approved_by.first_name:
                return obj.approved_by.first_name
            else:
                return obj.approved_by.username

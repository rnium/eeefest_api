from django.db import models
from django.contrib.auth.models import User


class Registration(models.Model):
    contest_choices = [
        ('lfr', "Line Follower Robot"),
        ('poster', "Poster Presentation"),
        ('circuit-solve', "Circuit Master"),
        ('integration', "Integration Bee"),
        ('gaming-fifa', "Gaming Contest FIFA"),
        ('gaming-chess', "Gaming Contest Chess"),
    ]
    gateways = [
        ('bkash', 'bKash'),
        ('rocket', 'DBBL Rocket'),
        ('nagad', 'Nagad'),
    ]
    contest = models.CharField(max_length=20, choices=contest_choices)
    team_name = models.CharField(max_length=500, null=True, blank=True)
    group_members_count = models.IntegerField(default=1)
    gateway = models.CharField(max_length=100, choices=gateways, null=True, blank=True)
    paying_number = models.CharField(max_length=100, null=True, blank=True)
    transaction_id = models.CharField(max_length=100, null=True, blank=True)
    ip_address = models.GenericIPAddressField()
    is_approved = models.BooleanField(default=False)
    is_email_sent = models.BooleanField(default=False)
    approved_by = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)
    approved_at = models.DateTimeField(null=True, blank=True)
    added_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    
class GroupMember(models.Model):
    controller_options = [
        ('keyb', 'Keyboard'),
        ('joys', 'Joystick'),
    ]
    registration = models.ForeignKey(Registration, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    inst = models.CharField(max_length=200)
    reg_num = models.CharField(max_length=200, null=True, blank=True)
    dept = models.CharField(max_length=100, null=True, blank=True)
    tshirt = models.CharField(max_length=5, null=True, blank=True)
    phone = models.CharField(max_length=20, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    game_controller = models.CharField(max_length=5, choices=controller_options, null=True, blank=True)
    
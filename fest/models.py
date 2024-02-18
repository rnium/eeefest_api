from django.db import models


class Registration(models.Model):
    contest_choices = [
        ('lfr', "Line Following"),
        ('poster', "Poster Presentation"),
        ('circuit-solve', "Circuit Solve"),
        ('integration', "Integration"),
        ('gaming-fifa', "Gaming [FIFA]"),
        ('gaming-chess', "Gaming [Chess]"),
    ]
    gateways = [
        ('rocket', 'DBBL Rocket'),
        ('nagad', 'Nagad'),
    ]
    contest = models.CharField(max_length=20, choices=contest_choices)
    name = models.CharField(max_length=500)
    team_name = models.CharField(max_length=500, null=True, blank=True)
    email = models.EmailField(max_length=500)
    phoneNumber = models.CharField(max_length=20)
    gateway = models.CharField(max_length=100, choices=gateways, default='rokcet')
    transaction_id = models.CharField(max_length=100)
    ip_address = models.GenericIPAddressField()

    

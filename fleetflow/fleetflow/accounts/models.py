from django.db import models

# Create your models here.
from django.contrib.auth.models import User

class RegistrationRequest(models.Model):
    STATUS = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]
    ROLE_CHOICES = [
        ('Manager', 'Manager'),
        ('Dispatcher', 'Dispatcher'),
        ('Safety Officer', 'Safety Officer'),
        ('Analyst', 'Analyst'),
    ]

    full_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=255)
    requested_role = models.CharField(max_length=50, choices=ROLE_CHOICES)
    status = models.CharField(max_length=20, choices=STATUS, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    reviewed_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.full_name} ({self.requested_role}) — {self.status}"
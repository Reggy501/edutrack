from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('teacher', 'Teacher'),
        ('parent', 'Parent'),
    ]

    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='teacher')
    phone = models.CharField(max_length=20, blank=True, null=True)
    school = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"{self.username} - {self.role}"

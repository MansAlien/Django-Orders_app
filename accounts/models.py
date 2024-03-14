from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    GENDER_CHOICES = {
            "M": "Male",
            "F": "Female"
    }

    age = models.PositiveIntegerField(null=True, blank=True)
    salary = models.PositiveIntegerField(null=True, blank=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)

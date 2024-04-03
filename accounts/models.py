from django.db.models import F
from django.db import models
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User

class JobTitle(models.Model):
    name = models.CharField(max_length=255)

class Department(models.Model):
    name = models.CharField(max_length=255)

class Country(models.Model):
    name = models.CharField(max_length=255)

class City(models.Model):
    name = models.CharField(max_length=255)
    country = models.ForeignKey(Country, on_delete=models.Set_NULL, null=True)

class UserProfile(models.Model):
    GENDER = {
        "M":"Male",
        "F":"Female",
    }
    user = models.One
    job_title = models.ForeignKey(JobTitle, on_delete=models.Set_NULL, null=True)
    department = models.ForeignKey(Department, on_delete=models.Set_NULL, null=True)
    city = models.ForeignKey(City, on_delete=models.Set_NULL, null=True)
    date_of_birth = models.DateField(null=True)
    start = models.DateField(null=True)
    address = models.TextField(null=True)
    gender = models.ChoiceField(max_length=1, choices=GENDER, default="M")

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.userprofile.save()

class DepartmentHistory(models.Model):
    department = models.ForeignKey(Department, on_delete=models.Set_NULL, null=True)
    user_profile = models.ForeignKey(UserProfile, on_delete=models.Set_NULL, null=True)
    start = models.DateField()
    end = models.DateField()

class JobHistory(models.Model):
    job_title = models.ForeignKey(Department, on_delete=models.Set_NULL, null=True)
    user_profile = models.ForeignKey(UserProfile, on_delete=models.Set_NULL, null=True)
    start = models.DateField()
    end = models.DateField()

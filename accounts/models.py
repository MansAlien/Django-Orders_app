from django.db.models import F
from django.db import models
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User

class JobTitle(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Department(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Country(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Governorate(models.Model):
    name = models.CharField(max_length=255)
    country = models.ForeignKey(Country, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.name

class City(models.Model):
    name = models.CharField(max_length=255)
    governorate = models.ForeignKey(Governorate, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.name

class UserProfile(models.Model):
    GENDER = {
        "M":"Male",
        "F":"Female",
    }
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    job_title = models.ForeignKey(JobTitle, on_delete=models.SET_NULL, null=True)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True)
    city = models.ForeignKey(City, on_delete=models.SET_NULL, null=True)
    date_of_birth = models.DateField(null=True)
    start = models.DateField(null=True)
    address = models.TextField(null=True)
    gender = models.CharField(max_length=1, choices=GENDER, default="M")

    def __str__(self):
        return self.user.username

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.userprofile.save()

class DepartmentHistory(models.Model):
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True)
    user_profile = models.ForeignKey(UserProfile, on_delete=models.SET_NULL, null=True)
    start = models.DateField()
    end = models.DateField()

    def __str__(self):
        return self.department.name

class JobTitleHistory(models.Model):
    job_title = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True)
    user_profile = models.ForeignKey(UserProfile, on_delete=models.SET_NULL, null=True)
    start = models.DateField()
    end = models.DateField()

    def __str__(self):
        return self.job_title.name

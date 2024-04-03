from django.db.models import F
from django.db import models
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User

class JobTitle(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    ROLE_CHOICES = [('Employee', 'Employee'), ('Admin', 'Admin'), ('Manager', 'Manager')]
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    salary_range_low = models.DecimalField(max_digits=10, decimal_places=2)
    salary_range_high = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.title

class StandardWorkSchedule(models.Model):
    name = models.CharField(max_length=255)
    start = models.TimeField()
    end = models.TimeField()
    hours = models.GeneratedField(
        expression = (F("end") - F("start"))/36000000000,
        output_field = models.FloatField(),
        db_persist = True,
    )    

    def __str__(self):
        return self.name

class UserProfile(models.Model):
    GENDER_CHOICES = [('M', 'Male'), ('F', 'Female')]
    MARITAL_STATUS_CHOICES = [('Single', 'Single'), ('Married', 'Married'), ('Divorced', 'Divorced'), ('Widowed', 'Widowed')]
    STATUS_CHOICES = [('Active', 'Active'), ('Inactive', 'Inactive'), ('Leave', 'Leave'), ('Terminated', 'Terminated')]

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    national_id = models.CharField(max_length=50, unique=True, blank=True, null=True)
    job_title = models.ForeignKey(JobTitle, on_delete=models.SET_NULL, null=True)
    schedule = models.ForeignKey(StandardWorkSchedule, on_delete=models.SET_NULL, null=True)
    hire_date = models.DateField(null=True)
    birth_date = models.DateField(null=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True, null=True)
    marital_status = models.CharField(max_length=8, choices=MARITAL_STATUS_CHOICES, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    phone = models.CharField(max_length=50, blank=True, null=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, null=True)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.username

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.userprofile.save()

class Department(models.Model):
    name = models.CharField(max_length=255)
    location = models.CharField(max_length=255, blank=True, null=True)
    manager = models.ForeignKey(UserProfile, on_delete=models.SET_NULL, null=True, blank=True, related_name='managed_departments')

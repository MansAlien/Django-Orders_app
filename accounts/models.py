from django.db.models import F
from django.db import models
from django.conf import settings
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.utils import timezone


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
    # department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True)
    city = models.ForeignKey(City, on_delete=models.SET_NULL, null=True)
    date_of_birth = models.DateField(null=True)
    start = models.DateField(null=True)
    address = models.TextField(null=True)
    gender = models.CharField(max_length=1, choices=GENDER, default="M")
    age = models.PositiveIntegerField(null=True)

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
    start = models.DateTimeField()
    end = models.DateTimeField()

    def __str__(self):
        return self.department.name

class JobTitleHistory(models.Model):
    job_title = models.ForeignKey(JobTitle, on_delete=models.SET_NULL, null=True)
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE, null=True)
    start = models.DateTimeField()
    end = models.DateTimeField(null=True)

    def __str__(self):
        return f"{self.user_profile} - {self.job_title} - {self.start}" 

@receiver(pre_save, sender=UserProfile)
def update_job_title_history(sender, instance, **kwargs):
    try:
        old_instance = UserProfile.objects.get(pk=instance.pk)
        print(old_instance)
    except UserProfile.DoesNotExist:
        # If UserProfile instance is being created, no need to update job title history
        return 
    
    # Check if job title has changed
    if old_instance.job_title != instance.job_title:
        # If job title changed, update the end date of the last job title history
        last_job_title_history = JobTitleHistory.objects.filter(user_profile=instance).order_by('start').last()
        print(JobTitleHistory.objects.filter(user_profile=instance).order_by('-start').all())
        if last_job_title_history:
            last_job_title_history.end = timezone.now()
            last_job_title_history.save()
            print(last_job_title_history.end)
            print(last_job_title_history.id)
            print("done")
        
        # Create a new job title history record
        JobTitleHistory.objects.create(
            user_profile=instance,
            job_title=instance.job_title,
            start=timezone.now(),
            end=None
        )
        print("created")

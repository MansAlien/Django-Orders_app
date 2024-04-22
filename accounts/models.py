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
    salary = models.PositiveIntegerField(null=True)

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
    start = models.DateTimeField(null=True)
    end = models.DateTimeField(null=True)

    def __str__(self):
        return f"{self.user_profile} - {self.job_title} - {self.start}" 

@receiver(post_save, sender=UserProfile)
def create_job_title_history(sender, instance, created, **kwargs):
    if created:
        job_title = instance.job_title
        start = instance.start 
        JobTitleHistory.objects.create(job_title=job_title, user_profile=instance, start=start)

@receiver(pre_save, sender=UserProfile)
def update_first_job_title_history(sender, instance, **kwargs):
    if instance.pk:  # Check if the instance is already in the database (i.e., being updated)
        original_instance = UserProfile.objects.get(pk=instance.pk)
        if original_instance.start != instance.start:
            # Get the first job title history associated with the profile
            first_job_title_history = instance.jobtitlehistory_set.first()
            if first_job_title_history and first_job_title_history.job_title == None:
                first_job_title_history.job_title = instance.job_title  # Update the job title
                first_job_title_history.start = instance.start  # Update the start time
                first_job_title_history.save()
            elif first_job_title_history.job_title != None:
                first_job_title_history.start = instance.start  # Update the start time
                first_job_title_history.save()
                pass

@receiver(pre_save, sender=UserProfile)
def update_job_title_history(sender, instance, **kwargs):
    if instance.pk:  # Check if the instance is already in the database (i.e., being updated)
        last_job_title_history = instance.jobtitlehistory_set.last()  # Get the last job title history
        if last_job_title_history:
            if last_job_title_history.job_title != instance.job_title:  # Check if job_title is changed
                last_job_title_history.end = timezone.now()  # End the current job title period
                last_job_title_history.save()
                # Create a new JobTitleHistory with the new job title
                JobTitleHistory.objects.create(
                    job_title=instance.job_title,
                    user_profile=instance,
                    start=timezone.now()
                )
                # Cancel the saving process to prevent UserProfile changes
                return


class SalaryHistory(models.Model):
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    amount = models.PositiveIntegerField(null=True)
    start = models.DateTimeField(null=True)
    end = models.DateTimeField(null=True)

    def __str__(self):
        return f"{self.user_profile} - {self.amount} - {self.start}"


@receiver(pre_save, sender=UserProfile)
def update_salary_history(sender, instance, **kwargs):
    try:
        old_instance = UserProfile.objects.get(pk=instance.pk)
    except UserProfile.DoesNotExist:
        # If UserProfile instance is being created, no need to update salary history
        return 
    
    # Check if salary has changed
    if old_instance.salary != instance.salary:
        # If salary changed, update the end date of the last salary history
        last_salary_history = SalaryHistory.objects.filter(user_profile=instance).order_by('start').last()
        if last_salary_history:
            last_salary_history.end = timezone.now()
            last_salary_history.save()
        
        # Create a new salary history record
        SalaryHistory.objects.create(
            user_profile=instance,
            amount=instance.salary,
            start=timezone.now(),
            end=None
        )

@receiver(pre_save, sender=UserProfile)
def update_first_salary_history(sender, instance, **kwargs):
    if instance.pk:  # Check if the instance is already in the database (i.e., being updated)
        original_instance = UserProfile.objects.get(pk=instance.pk)
        if original_instance.start != instance.start:
            # Get the first salary history associated with the profile
            first_salary_history = instance.salaryhistory_set.first()
            if first_salary_history:
                first_salary_history.start = instance.start  # Update the start time
                first_salary_history.save()

class Deduction(models.Model):
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    discription = models.TextField(default='')
    date = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.name

User = settings.AUTH_USER_MODEL

class LoggedInUser(models.Model):
    user = models.OneToOneField(User, related_name='logged_in_user')
    session_key = models.CharField(max_length=32, null=True, blank=True)

    def __str__(self):
        return self.user.username

@receiver(user_logged_in)
def on_user_logged_in(sender, request, **kwargs):
    LoggedInUser.objects.get_or_create(user=kwargs.get('user')) 


@receiver(user_logged_out)
def on_user_logged_out(sender, **kwargs):
    LoggedInUser.objects.filter(user=kwargs.get('user')).delete()

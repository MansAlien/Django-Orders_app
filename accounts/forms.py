from .models import UserProfile 
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm):
        model = UserProfile 
        fields = (
                "national_id",
                "job_title",
                "hire_date",
                "birth_date",
                "gender",
                "marital_status",
                "address",
                "phone",
                "status",
        )

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = UserProfile 
        fields = (
                "national_id",
                "job_title",
                "hire_date",
                "birth_date",
                "gender",
                "marital_status",
                "address",
                "phone",
                "status",
        )



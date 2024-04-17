from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import UserProfile


class UserCreationForm(UserCreationForm):
    username = forms.CharField(label='Username', max_length=100, widget=forms.TextInput(attrs={'autocomplete': 'username'}))
    email = forms.EmailField(label='Email', max_length=100, widget=forms.EmailInput(attrs={'autocomplete': 'email'}))
    first_name = forms.CharField(label='First Name', max_length=100, widget=forms.TextInput(attrs={'autocomplete': 'given-name'}))
    last_name = forms.CharField(max_length=30, required=True)
    is_active = forms.BooleanField(required=False, initial=True)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password1', 'password2', 'is_active']
        help_texts = {
            'username': None,
            'email': None,
            'password1': None,
            'password2': None,
        }

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['job_title', 'city', 'date_of_birth', 'start', 'address', 'gender', 'age', 'salary']

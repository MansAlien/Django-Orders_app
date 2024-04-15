from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class UserCreationForm(UserCreationForm):
    email = forms.EmailField()
    is_active = forms.BooleanField(required=False, initial=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'is_active']
        help_texts = {
            'username': None,
            'email': None,
            'password1': None,
            'password2': None,
        }

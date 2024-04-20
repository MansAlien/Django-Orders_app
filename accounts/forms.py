from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import UserProfile, Deduction
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, Field


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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('first_name', css_class='form-group col-md-6 mb-0'),
                Column('last_name', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            'username',
            'email',
            'password1',
            'password2',
            Field('is_active', css_class='form-check-input', template='your_app/custom_checkbox.html'),
        )



class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['job_title', 'city', 'date_of_birth', 'start', 'address', 'gender', 'age', 'salary']

class DeductionForm(forms.ModelForm):
    class Meta:
        model = Deduction
        fields = ['name', 'amount', 'discription']

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'is_active']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError('This email is already in use.')
        return email

class PasswordResetForm(forms.Form):
    new_password = forms.CharField(label='New Password', widget=forms.PasswordInput)
    confirm_password = forms.CharField(label='Confirm Password', widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super().clean()
        new_password = cleaned_data.get('new_password')
        confirm_password = cleaned_data.get('confirm_password')

        if new_password != confirm_password:
            raise forms.ValidationError("The new passwords do not match.")

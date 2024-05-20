from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import UserProfile, Deduction

class UserCreationForm(UserCreationForm):
    is_active = forms.BooleanField(required=False, initial=True)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2', 'is_active']
        help_texts = {
            'username': None,
            'email': None,
            'password1': None,
            'password2': None,
            "is_active": None,
        }

class UserProfileForm(forms.ModelForm):
    address = forms.CharField(widget=forms.Textarea(attrs={"rows": 3}))
    class Meta:
        model = UserProfile
        fields = ['job_title', 'city', 'date_of_birth', 'start', 'address', 'gender', 'age', 'salary']

class DeductionForm(forms.ModelForm):
    discription = forms.CharField(widget=forms.Textarea(attrs={"rows": 3}))
    class Meta:
        model = Deduction
        fields = ['name', 'amount', 'discription']

class DeductionEditForm(forms.ModelForm):
    discription = forms.CharField(widget=forms.Textarea(attrs={"rows": 3}))
    class Meta:
        model = Deduction
        fields = ['name', 'amount', 'discription', 'date']

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'is_active']
        help_texts = {
            'username': None,
            'email': None,
            "is_active": None,
        }

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

class PermissionForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        permissions = kwargs.pop('permissions', None)
        super(PermissionForm, self).__init__(*args, **kwargs)
        if permissions:
            self.fields['user_permissions'].queryset = permissions
            # Set the label of each checkbox to the codename of the permission
            for permission in permissions:
                self.fields['user_permissions'].label_from_instance = lambda obj: obj.codename
        self.fields['user_permissions'].label = ""
        self.fields['user_permissions'].help_text = ""

    class Meta:
        model = User
        fields = ('user_permissions',)
        widgets = {
            'user_permissions': forms.CheckboxSelectMultiple,
        }

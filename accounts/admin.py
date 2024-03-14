from django.contrib import admin
from .models import CustomUser
from .forms import CustomUserCreationForm, CustomUserChangeForm
from django.contrib.auth.admin import UserAdmin


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = [
            "username",
            "email",
            "age",
            "salary",
            "gender",
            "is_staff",
    ]
    fieldsets = UserAdmin.fieldsets + (( None, {"fields": ("age", "salary", "gender")}),)
    add_fieldsets = UserAdmin.add_fieldsets + (( None, {"fields": ("age", "salary", "gender")}),)

admin.site.register(CustomUser, CustomUserAdmin)


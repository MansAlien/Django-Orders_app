from django.contrib import admin
from .models import UserProfile , JobTitle, StandardWorkSchedule, Department
from django.contrib.auth.admin import UserAdmin


admin.site.register(UserProfile)
admin.site.register(JobTitle)
admin.site.register(StandardWorkSchedule)
admin.site.register(Department)


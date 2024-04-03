from django.contrib import admin
from .models import UserProfile , JobTitle, Department, JobTitleHistory, DepartmentHistory, City, Country
from django.contrib.auth.admin import UserAdmin



# vim: set fileencoding=utf-8 :
from django.contrib import admin

import accounts.models as models


class JobTitleAdmin(admin.ModelAdmin):

    list_display = ('id', 'name')
    list_filter = ('id', 'name')
    search_fields = ('name',)


class DepartmentAdmin(admin.ModelAdmin):

    list_display = ('id', 'name')
    list_filter = ('id', 'name')
    search_fields = ('name',)


class CountryAdmin(admin.ModelAdmin):

    list_display = ('id', 'name')
    list_filter = ('id', 'name')
    search_fields = ('name',)


class CityAdmin(admin.ModelAdmin):

    list_display = ('id', 'name', 'country')
    list_filter = ('country', 'id', 'name')
    search_fields = ('name',)


class UserProfileAdmin(admin.ModelAdmin):

    list_display = (
        'id',
        'user',
        'job_title',
        'department',
        'city',
        'date_of_birth',
        'start',
        'address',
        'gender',
    )
    list_filter = (
        'user',
        'job_title',
        'department',
        'city',
        'date_of_birth',
        'start',
        'id',
        'address',
        'gender',
    )


class DepartmentHistoryAdmin(admin.ModelAdmin):

    list_display = ('id', 'department', 'user_profile', 'start', 'end')
    list_filter = ('department', 'user_profile', 'start', 'end', 'id')


class JobTitleHistoryAdmin(admin.ModelAdmin):

    list_display = ('id', 'job_title', 'user_profile', 'start', 'end')
    list_filter = ('job_title', 'user_profile', 'start', 'end', 'id')


def _register(model, admin_class):
    admin.site.register(model, admin_class)


_register(models.JobTitle, JobTitleAdmin)
_register(models.Department, DepartmentAdmin)
_register(models.Country, CountryAdmin)
_register(models.City, CityAdmin)
_register(models.UserProfile, UserProfileAdmin)
_register(models.DepartmentHistory, DepartmentHistoryAdmin)
_register(models.JobTitleHistory, JobTitleHistoryAdmin)

from django.shortcuts import render, redirect 
from django.urls import reverse_lazy
from django.views.generic import  TemplateView, ListView
from django.views.generic.edit import  CreateView, UpdateView
from login_history.models import LoginHistory
from django.http import HttpResponse
from django.contrib.auth.models import User
from .models import UserProfile, JobTitleHistory, SalaryHistory, Deduction
from .forms import UserCreationForm, UserProfileForm, UserUpdateForm, PasswordResetForm, DeductionForm
from django.http import JsonResponse
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from .forms import PermissionForm
from django.contrib.auth.models import Permission
from django.db.models import Q
from django.contrib.auth.decorators import permission_required

##########################################################
#######                Forms                ##############
##########################################################
class SignUpView(CreateView):
   form_class = UserCreationForm
   success_url = reverse_lazy("admin:index")
   template_name = "registration/signup.html"

@permission_required("accounts.add_userprofile")
def create_user(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save() 
            return redirect('user_profile', pk=user.id)
    else:
        form = UserCreationForm()
    return render(request, 'settings/employee/modals/create_user.html', {'form': form})

@permission_required("accounts.change_userprofile")
def user_update_view(request, pk):
    user_instance = get_object_or_404(User, pk=pk)
    
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, instance=user_instance)
        if form.is_valid():
            form.save()
            return HttpResponse(status=204, headers={'HX-Trigger': 'info'})
    else:
        form = UserUpdateForm(instance=user_instance)
        
    return render(request, 'settings/employee/modals/edit_user.html', {'form': form})

@permission_required("accounts.add_userprofile")
def user_profile(request, pk):
    user = User.objects.get(id=pk)
    profile = UserProfile.objects.get(user=user)
    if request.method == "POST":
        form = UserProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            return HttpResponse(status=204, headers={'HX-Trigger': 'table_refresh, cards'})
            # Redirect or do whatever you need after the update
    else:
        form = UserProfileForm(instance=profile)
    return render(request, 'settings/employee/modals/create_user_profile.html', {'form': form, 'pk': pk})


@permission_required("accounts.change_userprofile")
def user_update_profile(request, pk):
    user = User.objects.get(id=pk)
    profile = UserProfile.objects.get(user=user)
    if request.method == "POST":
        form = UserProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            return HttpResponse(status=204, headers={'HX-Trigger': 'info'})
    else:
        form = UserProfileForm(instance=profile)
    return render(request, 'settings/employee/modals/edit_user.html', {'form': form})

@permission_required("accounts.change_userprofile")
def reset_password(request, user_id):
    user = User.objects.get(pk=user_id)
    if request.method == 'POST':
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            new_password = form.cleaned_data['new_password']
            # Reset the password for the user
            user.set_password(new_password)
            user.save()
            # Redirect or render success message
            return HttpResponse(status=204)
    else:
        form = PasswordResetForm()
    return render(request, 'settings/employee/modals/edit_user.html', {'form': form})

@permission_required("accounts.change_userprofile")
def create_deduction_view(request, pk):
    user = User.objects.get(id=pk)
    profile = UserProfile.objects.get(user=user)
    if request.method == 'POST':
        form = DeductionForm(request.POST)
        if form.is_valid():
            deduction = form.save(commit=False)
            deduction.user_profile = profile
            deduction.save()
            return HttpResponse(status=204, headers={'HX-Trigger': 'deduction_refresh'})
    else:
        form = DeductionForm()
    return render(request, 'settings/employee/modals/create_deduction.html', {'form': form})

@permission_required("accounts.change_userprofile")
def permission_view(request, pk):
    user = User.objects.get(id=pk)
    permissions = Permission.objects.filter(
        content_type__app_label='accounts',
        codename__endswith="_userprofile"
    ).exclude(codename__startswith="delete")
    
    if request.method == 'POST':
        form = PermissionForm(request.POST, instance=user, permissions=permissions)
        if form.is_valid():
            form.save()
            return HttpResponse(status=204, headers={'HX-Trigger': 'permissions_refresh'})
    else:
        form = PermissionForm(instance=user, permissions=permissions)
    
    return render(request, 'settings/employee/tabs/permissions.html', {'form': form, 'user': user})
##########################################################
#######                Refresh              ##############
##########################################################

@permission_required("accounts.view_userprofile")
def info_refresh(request, pk):
    user = UserProfile.objects.get(id=pk)
    job_title_history = JobTitleHistory.objects.filter(user_profile=user)
    salary_history = SalaryHistory.objects.filter(user_profile=user)
    context = {
            "user":user,
            "job_title_history":job_title_history,
            "salary_history":salary_history,
    }
    return render(request, "settings/employee/tabs/info.html", context)

@permission_required("accounts.view_userprofile")
def deduction_refresh(request, pk):
    user = UserProfile.objects.get(id=pk)
    deduction_list = Deduction.objects.filter(user_profile=user)
    context = {
            "user":user,
            "deduction_list":deduction_list,
    }
    return render(request, "settings/employee/tabs/deduction.html", context)

@permission_required("accounts.view_userprofile")
def table_refresh(request):
    user_profile = UserProfile.objects.all()
    logged_in_users = LoginHistory.objects.filter(is_logged_in=True).values_list('user__username', flat=True)
    context = {
        "userprofile_list": user_profile,
        "login_history": logged_in_users,
    }
    return render(request, "settings/employee/tables/table.html", context) 

@permission_required("accounts.view_userprofile")
def cards(request):
    admin_active = User.objects.filter(is_active=True).count()
    active = User.objects.filter(is_active=True, is_superuser=False).count()

    admin_inactive = User.objects.filter(is_active=False).count()
    inactive = User.objects.filter(is_active=False, is_superuser=False).count()

    admin_online = LoginHistory.objects.filter(is_logged_in=True).values_list('user__username', flat=True).count()
    online = LoginHistory.objects.filter(is_logged_in=True, user__is_superuser=False).values_list('user__username', flat=True).count()

    admin_offline = admin_active - admin_online
    offline = active - online
    context = {
        "admin_active":admin_active,
        "active":active,

        "admin_inactive":admin_inactive,
        "inactive":inactive,

        "admin_online":admin_online,
        "online":online,

        "admin_offline":admin_offline,
        "offline":offline,
    }
    return render(request, "settings/employee/cards.html", context) 




##########################################################
#######                Views                ##############
##########################################################

@permission_required("accounts.view_userprofile")
def employee_view(request):
    user_profile = UserProfile.objects.all()
    logged_in_users = LoginHistory.objects.filter(is_logged_in=True).values_list('user__username', flat=True)
    context = {
        "userprofile_list": user_profile,
        "login_history": logged_in_users,
    }
    return render(request, "settings/employee/employee.html", context) 

class EmployeeView(TemplateView):
    template_name = "settings/employee/employee.html"

@permission_required("accounts.view_userprofile")
def employee_detail_view(request, pk):
    user = UserProfile.objects.get(id=pk)
    job_title_history = JobTitleHistory.objects.filter(user_profile=user)
    salary_history = SalaryHistory.objects.filter(user_profile=user)
    login_history = LoginHistory.objects.filter(user=user.user)
    context = {
            "user":user,
            "job_title_history":job_title_history,
            "salary_history":salary_history,
            "login_history":login_history,
    }
    return render(request, "settings/employee/employee_detail.html", context) 


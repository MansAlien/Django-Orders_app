from django.shortcuts import render, redirect 
from django.urls import reverse_lazy
from django.views.generic import  TemplateView, ListView
from django.views.generic.edit import  CreateView, UpdateView
from .models import UserProfile, JobTitleHistory, SalaryHistory
from login_history.models import LoginHistory
from django.http import HttpResponse
from django.contrib.auth.models import User
from .forms import UserCreationForm, UserProfileForm, UserUpdateForm, PasswordResetForm
from django.http import JsonResponse
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404

##########################################################
#######                Forms                ##############
##########################################################
class SignUpView(CreateView):
   form_class = UserCreationForm
   success_url = reverse_lazy("admin:index")
   template_name = "registration/signup.html"

def create_user(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save() 
            return redirect('user_profile', pk=user.id)
    else:
        form = UserCreationForm()
    return render(request, 'settings/employee/modals/create_user.html', {'form': form})

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
    return render(request, 'settings/employee/modals/create_user_profile.html', {'form': form})

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



##########################################################
#######                Refresh              ##############
##########################################################

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


def table_refresh(request):
    user_profile = UserProfile.objects.all()
    logged_in_users = LoginHistory.objects.filter(is_logged_in=True).values_list('user__username', flat=True)
    context = {
        "userprofile_list": user_profile,
        "login_history": logged_in_users,
    }
    return render(request, "settings/employee/tables/table.html", context) 

def cards(request):
    active = User.objects.filter(is_active=True).count()
    inactive = User.objects.filter(is_active=False).count()
    online = LoginHistory.objects.filter(is_logged_in=True).values_list('user__username', flat=True).count()
    offline = active - online
    context = {
        "active":active,
        "inactive":inactive,
        "online":online,
        "offline":offline,
    }
    return render(request, "settings/employee/cards.html", context) 




##########################################################
#######                Views                ##############
##########################################################

class EmployeeView(ListView):
    model = UserProfile
    template_name = "settings/employee/employee.html"

def employee_view(request):
    user_profile = UserProfile.objects.all()
    logged_in_users = LoginHistory.objects.filter(is_logged_in=True).values_list('user__username', flat=True)
    active = User.objects.filter(is_active=True).count()
    inactive = User.objects.filter(is_active=False).count()
    online = LoginHistory.objects.filter(is_logged_in=True).values_list('user__username', flat=True).count()
    offline = active - online
    context = {
        "userprofile_list": user_profile,
        "login_history": logged_in_users,
        "active":active,
        "inactive":inactive,
        "online":online,
        "offline":offline,
    }
    return render(request, "settings/employee/employee.html", context) 

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


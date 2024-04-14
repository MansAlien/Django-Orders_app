from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView, ListView
from .models import UserProfile 
from django.contrib.auth.models import User
from login_history.models import LoginHistory

class SignUpView(CreateView):
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"

class EmployeeView(ListView):
    model = UserProfile
    template_name = "settings/employee/employee.html"

def employee_view(request):
    user_profile = UserProfile.objects.all()
    active = User.objects.filter(is_active=True).count()
    inactive = User.objects.filter(is_active=False).count()
    online = LoginHistory.objects.filter(is_logged_in=True).values_list('user__username', flat=True).count()
    offline = active - online
    logged_in_users = LoginHistory.objects.filter(is_logged_in=True).values_list('user__username', flat=True)
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
    context = {
            "user":user,
    }
    return render(request, "settings/employee/employee_detail.html", context) 

def info(request):
    return render(request, 'settings/employee/tabs/info.html')

def log(request):
    return render(request, 'settings/employee/tabs/log.html')

def permissions(request):
    return render(request, 'settings/employee/tabs/permissions.html')


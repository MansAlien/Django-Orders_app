from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView, ListView
from .models import UserProfile 
from login_history.models import LoginHistory

class SignUpView(CreateView):
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"

class EmployeeView(ListView):
    model = UserProfile
    template_name = "settings/employee/employee.html"

def employee_view(request):
    user_profile = UserProfile.objects.all()
    logged_in_users = LoginHistory.objects.filter(is_logged_in=True).values_list('user__username', flat=True)
    context = {
        "userprofile_list": user_profile,
        "login_history": logged_in_users,
    }
    return render(request, "settings/employee/employee.html", context) 


from django.shortcuts import render, redirect 
from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView, ListView
from .models import UserProfile 
from login_history.models import LoginHistory
from django.http import HttpResponse
from django.contrib.auth.models import User
from .forms import UserCreationForm, UserProfileForm
from django.http import JsonResponse

class EmployeeView(ListView):
    model = UserProfile
    template_name = "settings/employee/employee.html"

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

def table_refresh(request):
    user_profile = UserProfile.objects.all()
    logged_in_users = LoginHistory.objects.filter(is_logged_in=True).values_list('user__username', flat=True)
    context = {
        "userprofile_list": user_profile,
        "login_history": logged_in_users,
    }
    return render(request, "settings/employee/table.html", context) 

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

def modal_view(request):
    return render(request, 'settings/employee/modals/modal.html')

def step2_view(request):
    return HttpResponse('{% csrf_token %} <p>This is Step 2 content loaded via HTMX.</p>')

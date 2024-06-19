from functools import wraps
from django.shortcuts import redirect
from django.http import HttpResponseForbidden
from .models import UserProfile

def cashier_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')  # Redirect to login page if user is not authenticated
        if request.user.is_superuser:
            return view_func(request, *args, **kwargs)
        try:
            user_profile = UserProfile.objects.get(user=request.user)
            if user_profile.job_title.name == "Cashier":
                return view_func(request, *args, **kwargs)
            else:
                return HttpResponseForbidden("You do not have permission to access this page.")
        except UserProfile.DoesNotExist:
            return HttpResponseForbidden("You do not have permission to access this page.")
    return _wrapped_view

def editor_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')  # Redirect to login page if user is not authenticated
        if request.user.is_superuser:
            return view_func(request, *args, **kwargs)
        try:
            user_profile = UserProfile.objects.get(user=request.user)
            if user_profile.job_title.name == "Editor":
                return view_func(request, *args, **kwargs)
            else:
                return HttpResponseForbidden("You do not have permission to access this page.")
        except UserProfile.DoesNotExist:
            return HttpResponseForbidden("You do not have permission to access this page.")
    return _wrapped_view

from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView

class SignUpView(CreateView):
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"

class EmployeeView(TemplateView):
    template_name = "settings/employee/employee.html"

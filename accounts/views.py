from django.urls import reverse_lazy
from django.views.generic import CreateView

class SignUpView(CreateView):
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"

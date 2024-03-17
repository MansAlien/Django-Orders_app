from django.views.generic import ListView
from .models import Catigory

class CatigoryListView(ListView):
    model = Catigory
    template_name = "home.html"

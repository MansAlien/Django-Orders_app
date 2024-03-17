from django.views.generic import ListView
from .models import Catigory
from django.http.response import HttpResponse 
from django_htmx.http import HttpResponseClientRedirect
from django.shortcuts import render

class CatigoryListView(ListView):
    model = Catigory
    template_name = "home.html"


def view_categories(request):
    return HttpResponse("Hello there")

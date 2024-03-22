from django.views.generic import ListView, TemplateView
from .models import Category
from django.http.response import HttpResponse 
from django_htmx.http import HttpResponseClientRedirect
from django.shortcuts import render

class CategoryListView(ListView):
    model = Category
    template_name = "home.html"

class SettingsTemplateView(TemplateView):
    template_name="settings/settings.html"

def categoryview(request):
    category_list = Category.objects.all()
    context = {"category_list":category_list}
    return render(request, "settings/settings.html", context)


def createview(request):
    category_name = request.POST.get("category")
    category = Category.objects.create(name=category_name)
    category_list = Category.objects.all()
    context = {"category_list":category_list}
    return render(request, "settings/category/category.html", context)


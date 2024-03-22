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

def renameview(request, pk):
    category = Category.objects.get(id=pk)
    context = {"category":category}
    return render(request, "settings/category/category_edit.html", context)

def applyview(request, pk):
    category = Category.objects.get(id=pk)
    category.name = request.POST.get("update") 
    category.save()
    category_list = Category.objects.all()
    context = {"category_list":category_list}
    return render(request, "settings/category/category.html", context) 

def deleteview(request, pk):
    category = Category.objects.get(id=pk)
    category.delete()
    category_list = Category.objects.all()
    context = {"category_list":category_list}
    return render(request, "settings/category/category.html", context)

def cancelview(request):
    category_list = Category.objects.all()
    context = {"category_list":category_list}
    return render(request, "settings/category/category.html", context)



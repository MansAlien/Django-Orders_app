from django.views.generic import ListView, TemplateView
from .models import Category, Sub_Category 
from django.http.response import HttpResponse 
from django_htmx.http import HttpResponseClientRedirect
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from orders.forms import Sub_Category_Form 

@method_decorator(login_required, name='dispatch')
class HomeListView(ListView):
    model = Category
    template_name = "home.html"

@method_decorator(login_required, name='dispatch')
class SettingsTemplateView(TemplateView):
    template_name="settings/settings.html"

@login_required
def categoryview(request):
    category_list = Category.objects.all()
    subcategory_list = Sub_Category.objects.all()
    context = {"category_list":category_list, "subcategory_list":subcategory_list,}
    return render(request, "settings/category/category.html", context)


@login_required
def categorycreateview(request):
    category_name = request.POST.get("category")
    category = Category.objects.create(name=category_name)
    category_list = Category.objects.all()
    context = {"category_list":category_list}
    return render(request, "settings/category/category.html", context)

@login_required
def categoryrenameview(request, pk):
    category = Category.objects.get(id=pk)
    context = {"category":category}
    return render(request, "settings/category/category_edit.html", context)

@login_required
def categoryapplyview(request, pk):
    category = Category.objects.get(id=pk)
    category.name = request.POST.get("update") 
    category.save()
    category_list = Category.objects.all()
    context = {"category_list":category_list}
    return render(request, "settings/category/category.html", context) 

@login_required
def categorydeleteview(request, pk):
    category = Category.objects.get(id=pk)
    category.delete()
    category_list = Category.objects.all()
    context = {"category_list":category_list}
    return render(request, "settings/category/category.html", context)

@login_required
def categorycancelview(request):
    category_list = Category.objects.all()
    context = {"category_list":category_list}
    return render(request, "settings/category/category.html", context)

@login_required
def subcategoryview(request):
    category_id = request.POST.get("category_id")
    category = Category.objects.get(id=category_id)
    subcategory_list = category.sub_category_set.all()
    context = {"subcategory_list":subcategory_list}
    return render(request, "settings/category/subcategory.html" , context) 

@login_required
def subcategorycreateview(request):
    subcategory_name = request.POST.get("subcategory_name")
    category_id = request.POST.get("category_id")
    category = Category.objects.get(pk=category_id)
    category.sub_category_set.create(category=category_id, name=subcategory_name)
    subcategory_list = category.sub_category_set.all()
    context = {"subcategory_list":subcategory_list}
    return render(request, "settings/category/subcategory.html" , context) 

@login_required
def subcategoryrenameview(request, pk):
    subcategory = Sub_Category.objects.get(id=pk)
    context = {"subcategory":subcategory}
    return render(request, "settings/category/subcategory_edit.html", context)

@login_required
def subcategoryapplyview(request, pk):
    subcategory = Sub_Category.objects.get(id=pk)
    subcategory.name = request.POST.get("update_sub") 
    subcategory.save()
    subcategory_list = Sub_Category.objects.filter(category=subcategory.category.id)
    context = {"subcategory_list":subcategory_list}
    return render(request, "settings/category/subcategory.html", context) 

@login_required
def subcategorydeleteview(request, pk):
    subcategory = Sub_Category.objects.get(id=pk)
    subcategory.delete()
    subcategory_list = Sub_Category.objects.filter(category=subcategory.category.id)
    context = {"subcategory_list":subcategory_list}
    return render(request, "settings/category/subcategory.html", context) 

@login_required
def subcategorycancelview(request, pk):
    subcategory = Sub_Category.objects.get(id=pk)
    subcategory_list = Sub_Category.objects.filter(category=subcategory.category.id)
    context = {"subcategory_list":subcategory_list}
    return render(request, "settings/category/subcategory.html", context) 


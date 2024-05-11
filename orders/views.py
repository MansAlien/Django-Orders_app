from django.views.generic import ListView, TemplateView
from .models import Attribute, Category, Sub_Category, Product, ProductLine
from django.http.response import HttpResponse 
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from orders.forms import CategoryForm, SubCategoryForm , AttributeForm

@method_decorator(login_required, name='dispatch')
class HomeListView(ListView):
    model = Category
    template_name = "home.html"

@method_decorator(login_required, name='dispatch')
class SettingsTemplateView(TemplateView):
    template_name="settings/settings.html"

##########################################
######### Inventory Databases ############
##########################################

# Inventory
def inventory_view(request):
    category_list = Category.objects.all()
    context = {
        "category_list" : category_list
    }
    return render(request, "settings/inventory/inventory.html", context)

# Category
@login_required
def category_view(request):
    category_list = Category.objects.all()
    sub_category_list = Sub_Category.objects.all()
    context = {
        "category_list":category_list ,
        "sub_category_list":sub_category_list ,
    }
    return render(request, "settings/inventory/tabs/category.html", context)

def create_category(request):
    if request.method == "POST":
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponse(status=204, headers={"HX-Trigger": "category_refresh"})
    else:
        form = CategoryForm()
    return render(request, "settings/inventory/modals/create_category.html", {"form": form})

def edit_category(request, pk):
    category = Category.objects.get(id=pk)
    if request.method == "POST":
        form = CategoryForm(request.POST,  instance=category)
        if form.is_valid():
            form.save()
            return HttpResponse(status=204, headers={"HX-Trigger": "category_refresh"})
    else:
        form = CategoryForm(instance=category)
    return render( request, "settings/inventory/modals/edit_category.html", {"form": form, "pk":pk})

# SubCategory
def create_sub_category(request):
    if request.method == "POST":
        form = SubCategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponse(status=204, headers={"HX-Trigger": "category_refresh"})
    else:
        form = SubCategoryForm()
    return render(request, "settings/inventory/modals/create_sub_category.html", {"form": form})

def edit_sub_category(request, pk):
    sub_category = Sub_Category.objects.get(id=pk)
    if request.method == "POST":
        form = SubCategoryForm(request.POST,  instance=sub_category)
        if form.is_valid():
            form.save()
            return HttpResponse(status=204, headers={"HX-Trigger": "category_refresh"})
    else:
        form = SubCategoryForm(instance=sub_category)
    return render( request, "settings/inventory/modals/edit_sub_category.html", {"form": form, "pk":pk})

# Attributes
def attributes_view(request):
    attribute_list = Attribute.objects.all()
    product_list = Product.objects.all()
    context = {
        "attribute_list":attribute_list,
        "product_list":product_list,
    }
    return render(request, "settings/inventory/tabs/attributes.html", context)

def create_attribute(request):
    if request.method == "POST":
        form = AttributeForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponse(status=204, headers={"HX-Trigger": "attribute_refresh"})
    else:
        form = AttributeForm()
    return render(request, "settings/inventory/modals/create_attribute.html", {"form": form})

def edit_attribute(request, pk):
    attribute = Attribute.objects.get(id=pk)
    if request.method == "POST":
        form = AttributeForm(request.POST,  instance=attribute)
        if form.is_valid():
            form.save()
            return HttpResponse(status=204, headers={"HX-Trigger": "attribute_refresh"})
    else:
        form = AttributeForm(instance=attribute)
    return render(request, "settings/inventory/modals/edit_attribute.html", {"form": form, "pk":pk})

# product
def product_view(request):
    return render(request, "settings/inventory/tabs/product.html")

# product line
def product_line_view(request):
    return render(request, "settings/inventory/tabs/product_line.html")

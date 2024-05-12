from django.views.generic import ListView, TemplateView
from .models import Attribute, AttributeValue, Category, Sub_Category, Product, ProductLine
from django.http.response import HttpResponse 
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from orders.forms import CategoryForm, ProductLineForm, SubCategoryForm , AttributeForm, ProductForm, AttributeValueForm

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

def delete_category(request, pk):
    category = Category.objects.get(id=pk)
    category.delete()
    return HttpResponse(status=204, headers={"HX-Trigger": "category_refresh"})

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

def delete_sub_category(request, pk):
    sub_category = Sub_Category.objects.get(id=pk)
    sub_category.delete()
    return HttpResponse(status=204, headers={"HX-Trigger": "category_refresh"})

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

def delete_attribute(request, pk):
    attribute = Attribute.objects.get(id=pk)
    attribute.delete()
    return HttpResponse(status=204, headers={"HX-Trigger": "attribute_refresh"})

# Product
def create_product(request):
    if request.method == "POST":
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponse(status=204, headers={"HX-Trigger": "attribute_refresh"})
    else:
        form = ProductForm()
    return render(request, "settings/inventory/modals/create_product.html", {"form": form})

def edit_product(request, pk):
    product = Product.objects.get(id=pk)
    if request.method == "POST":
        form = ProductForm(request.POST,  instance=product)
        if form.is_valid():
            form.save()
            return HttpResponse(status=204, headers={"HX-Trigger": "attribute_refresh"})
    else:
        form = ProductForm(instance=product)
    return render(request, "settings/inventory/modals/edit_product.html", {"form": form, "pk":pk})

def delete_product(request, pk):
    product = Product.objects.get(id=pk)
    product.delete()
    return HttpResponse(status=204, headers={"HX-Trigger": "attribute_refresh"})

# Attribute value
def product_line_view(request):
    value_list = AttributeValue.objects.all() 
    product_line_list = ProductLine.objects.all()
    context = {
        "value_list":value_list,
        "product_line_list":product_line_list,
    }
    return render(request, "settings/inventory/tabs/product_line.html", context)

def create_attribute_value(request):
    if request.method == "POST":
        form = AttributeValueForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponse(status=204, headers={"HX-Trigger": "product_line_refresh"})
    else:
        form = AttributeValueForm()
    return render(request, "settings/inventory/modals/create_attribute_value.html", {"form": form})

def edit_attribute_value(request, pk):
    attribute_value = AttributeValue.objects.get(id=pk)
    if request.method == "POST":
        form = AttributeValueForm(request.POST,  instance=attribute_value)
        if form.is_valid():
            form.save()
            return HttpResponse(status=204, headers={"HX-Trigger": "product_line_refresh"})
    else:
        form = AttributeValueForm(instance=attribute_value)
    return render(request, "settings/inventory/modals/edit_attribute_value.html", {"form": form, "pk":pk})

def delete_attribute_value(request, pk):
    attribute_value = AttributeValue.objects.get(id=pk)
    attribute_value.delete()
    return HttpResponse(status=204, headers={"HX-Trigger": "product_line_refresh"})

# product line
def create_product_line(request):
    if request.method == "POST":
        form = ProductLineForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponse(status=204, headers={"HX-Trigger": "product_line_refresh"})
    else:
        form = ProductLineForm()
    return render(request, "settings/inventory/modals/create_product_line.html", {"form": form})

def edit_product_line(request, pk):
    product_line = ProductLine.objects.get(id=pk)
    if request.method == "POST":
        form = ProductLineForm(request.POST,  instance=product_line)
        if form.is_valid():
            form.save()
            return HttpResponse(status=204, headers={"HX-Trigger": "product_line_refresh"})
    else:
        form = ProductLineForm(instance=product_line)
    return render(request, "settings/inventory/modals/edit_product_line.html", {"form": form, "pk":pk})

def delete_product_line(request, pk):
    product_line = ProductLine.objects.get(id=pk)
    product_line.delete()
    return HttpResponse(status=204, headers={"HX-Trigger": "product_line_refresh"})

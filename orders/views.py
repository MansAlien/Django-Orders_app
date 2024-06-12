from django.db.models import ProtectedError, F
from django.views.generic import TemplateView
from accounts.models import UserProfile
from .models import Attribute, AttributeValue, Category, Sub_Category, Product, ProductLine, Customer, Order, Payment
from django.http.response import HttpResponse 
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from orders.forms import ( CategoryForm, ProductLineForm, ProductLineCreateForm, SubCategoryForm ,
                            AttributeForm, ProductForm, AttributeValueForm, CustomerForm, OrderDetailForm, PaymentForm )
from django.contrib import messages
from django.contrib.auth.decorators import permission_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

@login_required
def home_view(request):
    category_list = Category.objects.all()
    user_profile = UserProfile.objects.get(user=request.user)
    context = {
        "category_list" : category_list,
        "user_profile" : user_profile,
    }
    return render(request, "home.html", context)

@method_decorator(login_required, name='dispatch')
class SettingsTemplateView(TemplateView):
    template_name="settings/settings.html"

##########################################
######### Inventory Databases ############
##########################################

# Dashboard
@permission_required("orders.view_product")
def inventory_dashboard_view(request):
    to_buy_list = ProductLine.objects.filter(product__is_countable=True).exclude(stock_qty__gt=F('min_stock_qty'))
    product_line_list = ProductLine.objects.filter(product__is_countable=True)
    context = {
        "to_buy_list":to_buy_list,
        "product_line_list":product_line_list,
    }
    return render(request, "settings/dashboard/inventory.html", context)

# Inventory
@permission_required("orders.view_product")
def inventory_view(request):
    category_list = Category.objects.all()
    context = {
        "category_list" : category_list
    }
    return render(request, "settings/inventory/inventory.html", context)


# Category
@permission_required("orders.view_product")
def category_view(request):
    category_list = Category.objects.all()
    sub_category_list = Sub_Category.objects.all()
    context = {
        "category_list":category_list ,
        "sub_category_list":sub_category_list ,
    }
    return render(request, "settings/inventory/tabs/category.html", context)

@permission_required("orders.add_product")
def create_category(request):
    if request.method == "POST":
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponse(status=204, headers={"HX-Trigger": "category_refresh"})
        else:
            messages.error(request, "Item with this name already exists.")
            return HttpResponse(status=400, headers={"HX-Trigger": "category_refresh"})
    else:
        form = CategoryForm()
    return render(request, "settings/inventory/modals/create_category.html", {"form": form})

@permission_required("orders.change_product")
def edit_category(request, pk):
    category = Category.objects.get(id=pk)
    if request.method == "POST":
        form = CategoryForm(request.POST,  instance=category)
        if form.is_valid():
            form.save()
            return HttpResponse(status=204, headers={"HX-Trigger": "category_refresh"})
        else:
            messages.error(request, "Item with this name already exists.")
            return HttpResponse(status=400, headers={"HX-Trigger": "category_refresh"})
    else:
        form = CategoryForm(instance=category)
    return render( request, "settings/inventory/modals/edit_category.html", {"form": form, "pk":pk})

@permission_required("orders.change_product")
def delete_category(request, pk):
    try:
        category = Category.objects.get(id=pk)
        category.delete()
        return HttpResponse(status=204, headers={"HX-Trigger": "category_refresh"})
    except ProtectedError:
        messages.error(request,"Can't remove this item, it related to other items")
        return HttpResponse(status=204, headers={"HX-Trigger": "category_refresh"})

# SubCategory
@permission_required("orders.add_product")
def create_sub_category(request):
    if request.method == "POST":
        form = SubCategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponse(status=204, headers={"HX-Trigger": "category_refresh"})
        else:
            messages.error(request, "Item with this name already exists.")
            return HttpResponse(status=400, headers={"HX-Trigger": "category_refresh"})
    else:
        form = SubCategoryForm()
    return render(request, "settings/inventory/modals/create_sub_category.html", {"form": form})

@permission_required("orders.change_product")
def edit_sub_category(request, pk):
    sub_category = Sub_Category.objects.get(id=pk)
    if request.method == "POST":
        form = SubCategoryForm(request.POST,  instance=sub_category)
        if form.is_valid():
            form.save()
            return HttpResponse(status=204, headers={"HX-Trigger": "category_refresh"})
        else:
            messages.error(request, "Item with this name already exists.")
            return HttpResponse(status=400, headers={"HX-Trigger": "category_refresh"})
    else:
        form = SubCategoryForm(instance=sub_category)
    return render( request, "settings/inventory/modals/edit_sub_category.html", {"form": form, "pk":pk})

@permission_required("orders.change_product")
def delete_sub_category(request, pk):
    try:
        sub_category = Sub_Category.objects.get(id=pk)
        sub_category.delete()
        return HttpResponse(status=204, headers={"HX-Trigger": "category_refresh"})
    except ProtectedError:
        messages.error(request,"Can't remove this item, it related to other items")
        return HttpResponse(status=204, headers={"HX-Trigger": "category_refresh"})

# Attributes
@permission_required("orders.view_product")
def attributes_view(request):
    attribute_list = Attribute.objects.all()
    product_list = Product.objects.all()
    context = {
        "attribute_list":attribute_list,
        "product_list":product_list,
    }
    return render(request, "settings/inventory/tabs/attributes.html", context)

@permission_required("orders.add_product")
def create_attribute(request):
    if request.method == "POST":
        form = AttributeForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponse(status=204, headers={"HX-Trigger": "attribute_refresh"})
        else:
            messages.error(request, "Item with this name already exists.")
            return HttpResponse(status=400, headers={"HX-Trigger": "attribute_refresh"})
    else:
        form = AttributeForm()
    return render(request, "settings/inventory/modals/create_attribute.html", {"form": form})

@permission_required("orders.change_product")
def edit_attribute(request, pk):
    attribute = Attribute.objects.get(id=pk)
    if request.method == "POST":
        form = AttributeForm(request.POST,  instance=attribute)
        if form.is_valid():
            form.save()
            return HttpResponse(status=204, headers={"HX-Trigger": "attribute_refresh"})
        else:
            messages.error(request, "Item with this name already exists.")
            return HttpResponse(status=400, headers={"HX-Trigger": "attribute_refresh"})
    else:
        form = AttributeForm(instance=attribute)
    return render(request, "settings/inventory/modals/edit_attribute.html", {"form": form, "pk":pk})

@permission_required("orders.change_product")
def delete_attribute(request, pk):
    attribute = Attribute.objects.get(id=pk)
    attribute.delete()
    return HttpResponse(status=204, headers={"HX-Trigger": "attribute_refresh"})

# Product
@permission_required("orders.add_product")
def create_product(request):
    if request.method == "POST":
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponse(status=204, headers={"HX-Trigger": "attribute_refresh"})
        else:
            messages.error(request, "Item with this name already exists.")
            return HttpResponse(status=400, headers={"HX-Trigger": "attribute_refresh"})
    else:
        form = ProductForm()
    return render(request, "settings/inventory/modals/create_product.html", {"form": form})

@permission_required("orders.change_product")
def edit_product(request, pk):
    product = Product.objects.get(id=pk)
    if request.method == "POST":
        form = ProductForm(request.POST,  instance=product)
        if form.is_valid():
            form.save()
            return HttpResponse(status=204, headers={"HX-Trigger": "attribute_refresh"})
        else:
            messages.error(request, "Item with this name already exists.")
            return HttpResponse(status=400, headers={"HX-Trigger": "attribute_refresh"})
    else:
        form = ProductForm(instance=product)
    return render(request, "settings/inventory/modals/edit_product.html", {"form": form, "pk":pk})

@permission_required("orders.change_product")
def delete_product(request, pk):
    try:
        product = Product.objects.get(id=pk)
        product.delete()
        return HttpResponse(status=204, headers={"HX-Trigger": "attribute_refresh"})
    except ProtectedError:
        messages.error(request,"Can't remove this item, it related to other items")
        return HttpResponse(status=204, headers={"HX-Trigger": "attribute_refresh"})

# Attribute value
@permission_required("orders.view_product")
def product_line_view(request):
    value_list = AttributeValue.objects.all() 
    product_line_list = ProductLine.objects.all()
    context = {
        "value_list":value_list,
        "product_line_list":product_line_list,
    }
    return render(request, "settings/inventory/tabs/product_line.html", context)

@permission_required("orders.add_product")
def create_attribute_value(request):
    if request.method == "POST":
        form = AttributeValueForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponse(status=204, headers={"HX-Trigger": "product_line_refresh"})
    else:
        form = AttributeValueForm()
    return render(request, "settings/inventory/modals/create_attribute_value.html", {"form": form})

@permission_required("orders.change_product")
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

@permission_required("orders.change_product")
def delete_attribute_value(request, pk):
    attribute_value = AttributeValue.objects.get(id=pk)
    attribute_value.delete()
    return HttpResponse(status=204, headers={"HX-Trigger": "product_line_refresh"})

def create_product_line(request):
    product_list = Product.objects.all()
    if request.method == "POST":
        form = ProductLineCreateForm(request.POST)
        if form.is_valid():
            product_line = ProductLine(
                product=form.cleaned_data['product'],
                normal_price=form.cleaned_data['normal_price'],
                fawry_price=form.cleaned_data['fawry_price'],
                stock_qty=form.cleaned_data['stock_qty'],
                min_stock_qty=form.cleaned_data['min_stock_qty'],
                is_active=form.cleaned_data['is_active'],
                deliver_date=form.cleaned_data['deliver_date'],
                admin_comment=form.cleaned_data.get('admin_comment')
            )
            product_line.save()
            product_line.attribute_values.set(form.cleaned_data['attribute_values'])

            return HttpResponse(status=204, headers={"HX-Trigger": "product_line_refresh"})
        else:
            print(form.errors)  # Debugging statement to print form errors
    else:
        form = ProductLineCreateForm()
    context = {
        "product_list": product_list,
        "form": form,
    }
    return render(request, "settings/inventory/modals/create_product_line.html", context)

def load_product_values(request):
    product_id = request.GET.get("product")
    value_list = AttributeValue.objects.filter(product=product_id)
    return render(request, "settings/inventory/modals/product_values.html", {"value_list":value_list})

@permission_required("orders.change_product")
def edit_product_line(request, pk):
    product_line = ProductLine.objects.get(id=pk)
    if request.method == "POST":
        form = ProductLineForm(request.POST,  instance=product_line)
        if form.is_valid():
            form.save()
            return HttpResponse(status=204, headers={"HX-Trigger": "product_line_refresh"})
        else:
            print(form.errors)
            return HttpResponse(status=204, headers={"HX-Trigger": "product_line_refresh"})
    else:
        form = ProductLineForm(instance=product_line)
    return render(request, "settings/inventory/modals/edit_product_line.html", {"form": form, "pk":pk})

@permission_required("orders.change_product")
def delete_product_line(request, pk):
    try:
        product_line = ProductLine.objects.get(id=pk)
        product_line.delete()
        return HttpResponse(status=204, headers={"HX-Trigger": "product_line_refresh"})
    except ProtectedError:
        messages.error(request,"Can't remove this item, it related to other items")
        return HttpResponse(status=204, headers={"HX-Trigger": "product_line_refresh"})


# Cashier
@login_required
def cashier_view(request):
    category_list = Category.objects.all()
    context = {
        "category_list": category_list,
        "payment_form": PaymentForm()
    }
    return render(request, "cashier/home.html", context)


def product_list(request, pk):
    category = get_object_or_404(Category, pk=pk)
    sub_category_list = Sub_Category.objects.filter(category=category, is_active=True)
    subcategory_products = {}
    for sub in sub_category_list:
        product_list = Product.objects.filter(sub_category=sub, is_active=True)
        product_line_list = {product: ProductLine.objects.filter(product=product, is_active=True) for product in product_list}
        subcategory_products[sub] = product_line_list
    context = {
        "category": category,
        "subcategory_products": subcategory_products,
    }
    return render(request, "cashier/tables/product_list.html", context)



def new_order(request):
    customer_id = request.POST.get('customer_id')
    customer = Customer.objects.get(id=customer_id)
    order = Order.objects.create(customer=customer)
    context = {
        "order_id": order.id,
    }
    return render(request, "cashier/forms/order_info.html", context)


def order_detail_row(request, pk):
    product_line = ProductLine.objects.get(id=pk)
    form = OrderDetailForm()
    context = {
        "product_line": product_line,
        "form": form,
        "pk": pk,
    }
    return render(request, "cashier/tables/order_detail_row.html", context)

@csrf_exempt
def order_details_view(request):
    if request.method == 'POST':
        body_unicode = request.body.decode('utf-8')
        body_data = json.loads(body_unicode)
        
        order_id = body_data.get('order_id')
        rows = body_data.get('rows', [])

        for i in range(0, len(rows), 5):
            row_data=rows[i]
            product_line_id=row_data['product_line_id']
            product_line = ProductLine.objects.get(id=product_line_id)
            order = Order.objects.get(id=order_id)

            row_data=dict(list(row_data.items())[1:])
            form = OrderDetailForm(row_data)
            if form.is_valid():
                order_detail = form.save(commit=False)
                order_detail.product_line = product_line
                order_detail.order = order
                order_detail.save()
            else:
                print(form.errors)

        return HttpResponse(status=204, headers={"HX-Trigger": "payment_submit"})

    return JsonResponse({'status': 'invalid request'}, status=400)

def order_payment(request):
    order_id = request.POST.get('order_id')
    if request.method == "POST":
        order = Order.objects.get(id=order_id)
        form = PaymentForm(request.POST)
        if form.is_valid():
            payment = form.save(commit=False)
            payment.order = order
            payment.save()
            return HttpResponse(status=204)
        else:
            print(form.cleaned_data)
            print(form.errors)
            return HttpResponse(status=204)
    return render(request, "cashier/tables/order_detail_row.html")

# Cashier Settings

def cashier_settings_view(request):
    return render(request, "settings/cashier/cashier.html")

# Customer
def customer_view(request):
    customers = Customer.objects.all()
    context = {
        "customers":customers,
    }
    return render(request, "settings/cashier/tabs/customer.html", context)

def create_customer(request):
    if request.method == "POST":
        form = CustomerForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,"The new Customer Successfully Created")
            return HttpResponse(status=204, headers={"HX-Trigger": "customer_info"})
    else:
        form = CustomerForm()
    context = {
        "form":form,
    }
    return render(request, "cashier/modals/create_customer.html", context)

def delete_customer(request, pk):
    try:
        customer = Customer.objects.get(id=pk)
        customer.delete()
        return HttpResponse(status=204, headers={"HX-Trigger": "customer_info"})
    except ProtectedError:
        messages.error(request,"Can't remove this item, it related to other items")
        return HttpResponse(status=204, headers={"HX-Trigger": "customer_info"})

def edit_customer(request, pk):
    customer = Customer.objects.get(id=pk)
    if request.method == "POST":
        form = CustomerForm(request.POST,  instance=customer)
        if form.is_valid():
            form.save()
            messages.success(request,"The new Customer Successfully Updated")
            return HttpResponse(status=204, headers={"HX-Trigger": "clear"})
    else:
        form = CustomerForm(instance=customer)
    return render(request, "cashier/modals/edit_customer.html", { "form":form, "pk":pk})

def customer_info(request):
    customer = Customer.objects.last()
    context = {
        "customer":customer,
    }
    return render(request, "cashier/forms/customer_info.html", context)

def customer_with_id(request):
    customer_id = request.POST.get('customer_id')
    customer = None
    try:
        customer = Customer.objects.get(id=customer_id)
    except Customer.DoesNotExist:
        try:
            customer = Customer.objects.get(phone=customer_id)
        except Customer.DoesNotExist:
            customer = None
    if customer:
        context = {
            "customer": customer,
        }
        return render(request, "cashier/forms/customer_info.html", context)
    else:
        messages.error(request, "This customer does not exist.")
        return clear_customer_info(request)

def clear_customer_info(request):
    return render(request, "cashier/forms/customer_info.html")

# Order
def order_view(request):
    order_list = Payment.objects.all()
    context = {
        "order_list":order_list,
    }
    return render(request, "settings/cashier/tabs/orders.html", context)

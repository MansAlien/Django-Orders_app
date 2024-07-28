from django.db.models import ProtectedError, F
from django.views.generic import TemplateView
from accounts.models import UserProfile
from .models import Attribute, AttributeValue, Category, OrderDetail, Sub_Category, Product, ProductLine, Customer, Order, Payment, Comment, UploadImage
from django.http.response import HttpResponse 
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from orders.forms import ( CategoryForm, CommentForm, ProductLineForm, ProductLineCreateForm, SubCategoryForm ,
                            AttributeForm, ProductForm, AttributeValueForm, CustomerForm, OrderDetailForm, UpdateOrderDetailForm, PaymentForm, UploadImageForm )
from django.contrib import messages
from django.contrib.auth.decorators import permission_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import os
from django.http import Http404
from accounts.decorators import cashier_required, editor_required
from django.db.models import Q
import requests
from datetime import date, timedelta


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
@cashier_required
def cashier_view(request):
    category_list = Category.objects.all()
    context = {
        "category_list": category_list,
        "payment_form": PaymentForm()
    }
    return render(request, "cashier/home.html", context)


@cashier_required
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



@cashier_required
def new_order(request):
    customer_id = request.POST.get('customer_id')
    customer = Customer.objects.get(id=customer_id)
    order = Order.objects.create(customer=customer)
    # Extract year, month, and day from the created_at timestamp
    created_at = order.created_at
    year = created_at.year
    month = created_at.month
    day = created_at.day

    BASE_DIR = os.path.expanduser("~")
    base_dir = os.path.join(BASE_DIR, 'orders')
    folder_path = os.path.join(base_dir, str(year), str(month).zfill(2), str(day).zfill(2), str(order.id))
    order.path = folder_path
    order.save()

    # Create directories if they don't exist
    os.makedirs(folder_path, exist_ok=True)

    context = {
        "order_id": order.id,
    }
    return render(request, "cashier/forms/order_info.html", context)


@cashier_required
def order_detail_row(request, pk):
    product_line = ProductLine.objects.get(id=pk)
    form = OrderDetailForm()
    context = {
        "product_line": product_line,
        "form": form,
        "pk": pk,
    }
    return render(request, "cashier/tables/order_detail_row.html", context)

@cashier_required
def get_order_details(request):
    order_id = request.GET.get('order_id')
    try:
        order = Order.objects.get(id=order_id)
        order_details = OrderDetail.objects.filter(order=order)
        forms_and_product_lines = []
        for order_detail in order_details:
            form = UpdateOrderDetailForm(instance=order_detail)
            forms_and_product_lines.append((
                form, 
                order_detail.product_line, 
                order_detail.id, 
            ))
        context = {
            'forms': forms_and_product_lines,
        }       
        return render(request, "cashier/tables/update_order_details.html", context)
    except:
        messages.error(request, "Order not found.")
        return HttpResponse(status=204, headers={"HX-Trigger": "sdf"})

@cashier_required
def upload_image(request, detail_id):
    if request.method == 'POST':
        form = UploadImageForm(request.POST, request.FILES)
        if form.is_valid():
            order_detail = OrderDetail.objects.get(id=detail_id)
            image = form.save(commit=False)
            image.order_detail = order_detail
            image.author = request.user
            image.save()
            messages.success(request, "Image uploaded successfully.")
        else:
            messages.error(request, "Error uploading image.")
    return redirect('get_order_details')

def merge_dicts(dict_list):
    merged_dict = {}
    for d in dict_list:
        merged_dict.update(d)
    return merged_dict

@csrf_exempt
@cashier_required
def order_details_view(request):
    if request.method == 'POST':
        body_unicode = request.body.decode('utf-8')
        body_data = json.loads(body_unicode)
        order_id = body_data.get('order_id')
        rows = body_data.get('rows', [])
        chunk_size = 5
        merged_rows = [merge_dicts(rows[i:i + chunk_size]) for i in range(0, len(rows), chunk_size)]

        for row in merged_rows:
            product_line_id = row['product_line_id']
            order_detail_id = row.get('order_detail_id')
            product_line = ProductLine.objects.get(id=product_line_id)
            order = Order.objects.get(id=order_id)
            row_data = dict(list(row.items())[1:])  # Remove the product_line_id and order_detail_id from row_data
            
            if order_detail_id: #if the order_detail is exist update the data
                try:
                    order_detail = OrderDetail.objects.get(id=order_detail_id, order=order)
                    previous_amount = order_detail.amount
                    form = OrderDetailForm(row_data, instance=order_detail)
                except OrderDetail.DoesNotExist:
                    form = OrderDetailForm(row_data)
                    order_detail = form.save(commit=False)
            else: #if the order_detail is not exist create a new one
                if not row_data["deliver_date"]:
                    row_data["deliver_date"] = date.today()
                    row_data["deliver_date"] += timedelta(days=product_line.deliver_date)
                if not row_data["deliver_time"]:
                    row_data["deliver_time"] = "06:00"
                form = OrderDetailForm(row_data)
                order_detail = form.save(commit=False)
                previous_amount = 0

            if form.is_valid():
                if order_detail_id:
                    # Adjust the stock quantity based on the change in amount
                    change_in_amount = order_detail.amount - previous_amount
                    product_line.stock_qty -= change_in_amount
                else:
                    # Decrease the stock quantity by the amount for new order_detail
                    product_line.stock_qty -= order_detail.amount

                order_detail.product_line = product_line
                order_detail.order = order
                order_detail.save()
                product_line.save()

        return HttpResponse(status=204, headers={"HX-Trigger": "payment_submit"})

    return JsonResponse({'status': 'invalid request'}, status=400)


def delete_order_detail(request, pk):
    try:
        order_detail = OrderDetail.objects.get(id=pk)
        product_line = order_detail.product_line

        # Increase the product_line stock by 1
        product_line.stock_qty += order_detail.amount
        product_line.save()

        order_detail.delete()
        return HttpResponse(status=204)
    except OrderDetail.DoesNotExist:
        return JsonResponse({'status': 'Order detail not found'}, status=404)



@cashier_required
def order_payment(request):
    if request.method == "POST":
        order_id = request.POST.get('payment_order_id')
        payment_id = request.POST.get('payment_id')
        order = get_object_or_404(Order, id=order_id)

        if payment_id:
            payment = get_object_or_404(Payment, id=payment_id, order=order)
            form = PaymentForm(request.POST, instance=payment)
        else:
            form = PaymentForm(request.POST)

        if form.is_valid():
            payment = form.save(commit=False)
            payment.order = order
            if payment.paid is None:
                payment.paid = 0
            if payment.discount is None:
                payment.discount = 0
            payment.save()
            messages.success(request, f"The Order is Successfully Created: {payment.order.id}")
            return redirect('cashier')
    return render(request, "cashier/tables/order_detail_row.html")

@cashier_required
def get_order_payment(request):
    order_id = request.POST.get('payment_order_id')
    try:
        order = Order.objects.get(id=order_id)
        payment = Payment.objects.get(order=order)
        form = PaymentForm(instance=payment)
    except :
        messages.error(request, "Order Payment not found.")
        form = PaymentForm()
        return render(request, "cashier/forms/create_payment_form.html", {"payment_form":form})

    context = {
        'payment_form': form,
        'payment_id': payment.id,
        'order_id': order_id,
    }
    return render(request, "cashier/forms/update_payment_form.html", context)

# Cashier Settings
@permission_required("orders.view_order")
def cashier_settings_view(request):
    return render(request, "settings/cashier/cashier.html")

# Customer
@permission_required("orders.view_order")
def customer_view(request):
    customers = Customer.objects.all()
    context = {
        "customers":customers,
    }
    return render(request, "settings/cashier/tabs/customer.html", context)

@login_required
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

@permission_required("orders.change_order")
def delete_customer(request, pk):
    try:
        customer = Customer.objects.get(id=pk)
        customer.delete()
        return HttpResponse(status=204, headers={"HX-Trigger": "customer_info"})
    except ProtectedError:
        messages.error(request,"Can't remove this item, it related to other items")
        return HttpResponse(status=204, headers={"HX-Trigger": "customer_info"})

@login_required
def edit_customer(request, pk):
    customer = Customer.objects.get(id=pk)
    if request.method == "POST":
        form = CustomerForm(request.POST,  instance=customer)
        if form.is_valid():
            form.save()
            return HttpResponse(status=204)
    else:
        form = CustomerForm(instance=customer)
    return render(request, "cashier/modals/edit_customer.html", { "form":form, "pk":pk})

@login_required
def customer_info(request):
    customer = Customer.objects.last()
    context = {
        "customer":customer,
    }
    return render(request, "cashier/forms/customer_info.html", context)


@login_required
def customer_with_order(request):
    order_id = request.POST.get('order_id')
    if not order_id:
        messages.error(request, "Order ID is required.")
        return clear_customer_info(request)
    
    try:
        order_id = int(order_id)
    except ValueError:
        messages.error(request, "Invalid Order ID format.")
        return clear_customer_info(request)

    try:
        order = Order.objects.get(id=order_id)
        customer = order.customer
    except Order.DoesNotExist:
        messages.error(request, "Order Customer not found.")
        return clear_customer_info(request)
    
    if customer:
        context = {
            "customer": customer,
        }
        return render(request, "cashier/forms/customer_info.html", context)
    else:
        messages.error(request, "This customer does not exist.")
        return clear_customer_info(request)

@login_required
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
    context = {
        "customer": None,
    }
    return render(request, "cashier/forms/customer_info.html", context)

# Order
@permission_required("orders.view_order")
def order_view(request):
    order_list = Payment.objects.all().order_by("-order__created_at")
    context = {
        "order_list":order_list,
    }
    return render(request, "settings/cashier/tabs/orders.html", context)

@permission_required("orders.view_order")
def order_details_list(request, pk):
    order = Order.objects.get(id=pk)
    order_details_list = OrderDetail.objects.filter(order=order)
    payment = Payment.objects.get(order=order)
    comment_list = Comment.objects.filter(order=order).order_by("-created_at")
    comment_count = Comment.objects.filter(order=order).count()
    context = {
        "order_details_list":order_details_list,
        "order":order,
        "payment":payment,
        "comment_list":comment_list,
        "comment_count":comment_count,
    }
    return render(request, "settings/cashier/tabs/order_details.html", context)

@login_required
def create_comment(request, pk):
    order=Order.objects.get(id=pk)
    user = request.user
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment=form.save(commit=False)
            comment.order=order
            comment.user=user
            comment.save()
            messages.success(request,"The comment is created successfully")
            return HttpResponse(status=204, headers={"HX-Trigger": "order_details_refresh","HX-Trigger": "refresh_comments"})
    else:
        form = CommentForm()
    context = {
        "form":form,
        "pk":pk,
    }
    return render(request, "settings/cashier/modals/create_comment.html", context)


@login_required
def edit_comment(request, pk):
    comment = Comment.objects.get(id=pk)
    if request.method == "POST":
        form = CommentForm(request.POST,  instance=comment)
        if form.is_valid():
            form.save()
            messages.success(request,"The comment is updated successfully")
            return HttpResponse(status=204, headers={"HX-Trigger": "order_details_refresh","HX-Trigger": "refresh_comments"})
    else:
        form = CommentForm(instance=comment)
    context = {
        "form":form,
        "pk":pk,
    }
    return render(request, "settings/cashier/modals/edit_comment.html", context)

@login_required
def delete_comment(request, pk):
    try:
        comment = Comment.objects.get(id=pk)
        comment.delete()
        messages.success(request,"The comment is deleted successfully")
        return HttpResponse(status=204, headers={"HX-Trigger": "order_details_refresh", "HX-Trigger": "refresh_comments"})
    except ProtectedError:
        messages.error(request,"Can't remove this item, it related to other items")
        return HttpResponse(status=204, headers={"HX-Trigger": "order_details_refresh", "HX-Trigger": "refresh_comments"})

# Editor 
@editor_required
def editor_view(request):
    return render(request, "editor/editor.html")

@editor_required
def editor_table_refresh(request):
    order_list=Payment.objects.filter(order__delivery_status="P").order_by('-order__created_at')
    context={
        "order_list":order_list
    }
    return render(request, "editor/tables/orders_table.html", context)

@editor_required
def editor_order_details(request, pk):
    order=Order.objects.get(id=pk)
    order_details_list=OrderDetail.objects.filter(order=order)
    context={
        "order":order,
        "order_details_list":order_details_list,
    }
    return render(request, "editor/editor_order_details.html", context)

@login_required
def editor_comments(request, pk):
    order=Order.objects.get(id=pk)
    comment_list=Comment.objects.filter(order=order).order_by("-created_at")
    comment_count=Comment.objects.filter(order=order).count()
    context={
        "order":order,
        "comment_list":comment_list,
        "comment_count":comment_count,
    }
    return render(request, "editor/comments.html", context)

@login_required
def serve_order_file(request, order_id):
    try:
        order = Order.objects.get(id=order_id)
        file_path = order.path

        # Send request to Flask server running on host machine
        response = requests.post('http://host.docker.internal:5000/open_folder', json={"file_path": file_path})
        if response.status_code == 200:
            return HttpResponse(status=204)
        else:
            return HttpResponse(response.json(), status=response.status_code)
    except Order.DoesNotExist:
        raise Http404("Order does not exist")

@login_required
def open_folder(request):
    order_id = request.POST.get('order_id')
    try:
        order = Order.objects.get(id=order_id)
        file_path = order.path

        # Send request to Flask server running on host machine
        response = requests.post('http://host.docker.internal:5000/open_folder', json={"file_path": file_path})
        if response.status_code == 200:
            return HttpResponse(status=204)
        else:
            return HttpResponse(response.json(), status=response.status_code)
    except Order.DoesNotExist:
        raise Http404("Order does not exist")

def search_orders(request):
    query = request.GET.get('query', '')
    filter_type = request.GET.get('filter_type', 'id')
    
    if query:
        if filter_type == 'id':
            orders = Order.objects.filter(id__icontains=query).order_by('-created_at')
        elif filter_type == 'date':
            orders = Order.objects.filter(created_at__icontains=query).order_by('-created_at')
        elif filter_type == 'name':
            orders = Order.objects.filter(
                Q(customer__name_one__icontains=query) |
                Q(customer__name_two__icontains=query)
            ).order_by('-created_at')
        elif filter_type == 'phone':
            orders = Order.objects.filter(
                Q(customer__phone__icontains=query) |
                Q(customer__whatsapp__icontains=query)
            ).order_by('-created_at')
    else:
        orders = Order.objects.filter(payment__order__id__icontains=query).order_by('-created_at')
    
    return render(request, 'editor/tables/partial_order_list.html', {'order_list': orders})

def bill(request):
    order_id = request.POST.get('order_id')
    print(order_id)
    order = Order.objects.get(id=order_id)
    order_details = OrderDetail.objects.filter(order=order)
    payment = Payment.objects.filter(order=order).last()
    context={
        "order":order,
        "order_details":order_details,
        "payment":payment,
    }
    return render(request, 'cashier/modals/bill.html', context)



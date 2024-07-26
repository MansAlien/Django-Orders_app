from import_export.admin import ImportExportModelAdmin
from django.contrib import admin
import orders.models as models


class CategoryAdmin(ImportExportModelAdmin, admin.ModelAdmin):

    list_display = ('id', 'name', 'is_active')
    list_filter = ('is_active', 'id', 'name')
    search_fields = ('name',)


class Sub_CategoryAdmin(ImportExportModelAdmin, admin.ModelAdmin):

    list_display = ('id', 'category', 'name', 'is_active')
    list_filter = ('category', 'is_active', 'id', 'name')
    search_fields = ('name',)


class AttributeAdmin(ImportExportModelAdmin, admin.ModelAdmin):

    list_display = ('id', 'name', 'description')
    list_filter = ('id', 'name', 'description')
    search_fields = ('name',)


class ProductAdmin(ImportExportModelAdmin, admin.ModelAdmin):

    list_display = (
        'id',
        'sub_category',
        'name',
        'description',
        'is_active',
        'is_countable',
        'created_at',
        'updated_at',
    )
    list_filter = (
        'sub_category',
        'is_active',
        'is_countable',
        'created_at',
        'updated_at',
        'id',
        'name',
        'description',
    )
    search_fields = ('name',)
    date_hierarchy = 'created_at'


class AttributeValueAdmin(ImportExportModelAdmin, admin.ModelAdmin):

    list_display = ('id', 'product', 'attribute', 'attribute_value')
    list_filter = ('product', 'attribute', 'id', 'attribute_value')


class ProductLineAdmin(ImportExportModelAdmin, admin.ModelAdmin):

    list_display = (
        'id',
        'product',
        'normal_price',
        'fawry_price',
        'stock_qty',
        'min_stock_qty',
        'is_active',
        'deliver_date',
        'admin_comment',
    )
    list_filter = (
        'product',
        'is_active',
        'id',
        'normal_price',
        'fawry_price',
        'stock_qty',
        'min_stock_qty',
        'deliver_date',
        'admin_comment',
    )
    raw_id_fields = ('attribute_values',)


class CustomerAdmin(ImportExportModelAdmin, admin.ModelAdmin):

    list_display = ('id', 'name_one', 'name_two', 'phone', 'whatsapp')
    list_filter = ('id', 'name_one', 'name_two', 'phone', 'whatsapp')


class OrderAdmin(ImportExportModelAdmin, admin.ModelAdmin):

    list_display = (
        'id',
        'customer',
        'delivery_status',
        'is_active',
        'created_at',
    )
    list_filter = (
        'customer',
        'is_active',
        'created_at',
        'id',
        'delivery_status',
    )
    date_hierarchy = 'created_at'


class OrderDetailAdmin(ImportExportModelAdmin, admin.ModelAdmin):

    list_display = (
        'id',
        'order',
        'product_line',
        'deliver_type',
        'delivery_Status',
        'is_active',
        'amount',
        'customer_comment',
        'location',
        'created_at',
        'updated_at',
        'deliver_date',
    )
    list_filter = (
        'order',
        'product_line',
        'is_active',
        'created_at',
        'updated_at',
        'deliver_date',
        'id',
        'deliver_type',
        'delivery_Status',
        'amount',
        'customer_comment',
        'location',
    )
    date_hierarchy = 'created_at'


class PaymentAdmin(ImportExportModelAdmin, admin.ModelAdmin):

    list_display = (
        'id',
        'order',
        'discount',
        'total',
        'paid',
        'payment_method',
    )
    list_filter = (
        'order',
        'id',
        'discount',
        'total',
        'paid',
        'payment_method',
    )


class CommentAdmin(ImportExportModelAdmin, admin.ModelAdmin):

    list_display = ('id', 'user', 'order', 'content', 'created_at')
    list_filter = ('user', 'order', 'created_at', 'id', 'content')
    date_hierarchy = 'created_at'


def _register(model, admin_class):
    admin.site.register(model, admin_class)


_register(models.Category, CategoryAdmin)
_register(models.Sub_Category, Sub_CategoryAdmin)
_register(models.Attribute, AttributeAdmin)
_register(models.Product, ProductAdmin)
_register(models.AttributeValue, AttributeValueAdmin)
_register(models.ProductLine, ProductLineAdmin)
_register(models.Customer, CustomerAdmin)
_register(models.Order, OrderAdmin)
_register(models.OrderDetail, OrderDetailAdmin)
_register(models.Payment, PaymentAdmin)
_register(models.Comment, CommentAdmin)


from .models import UploadImage

@admin.register(UploadImage)
class TestImageAdmin(admin.ModelAdmin):
    list_display = ('id', 'author', 'image', 'uploaded_at')

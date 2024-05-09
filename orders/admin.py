from import_export.admin import ImportExportModelAdmin
from django.contrib import admin
import orders.models as models


class CategoryAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('id', 'name', 'is_active')
    list_filter = ('id', 'name', 'is_active')
    search_fields = ('name',)


class Sub_CategoryAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('id', 'category', 'name', 'is_active')
    list_filter = ('id', 'category', 'name', 'is_active')
    search_fields = ('name',)

class ProductAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('id', 'sub_category', 'name', 'description', 'is_active', 'is_countable', 'created_at', 'updated_at', 'stock_status')
    list_filter = ('id', 'sub_category', 'name', 'description', 'is_active', 'is_countable', 'created_at', 'updated_at', 'stock_status')
    search_fields = ('name',)

class ProductLineAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('id', 'product_with_attributes', 'price', 'stock_qty', 'is_active')
    search_fields = ('name',)

    def product_with_attributes(self, obj):
        attribute_values_str = ', '.join(str(attr_value.attribute_value) for attr_value in obj.attribute_values.all())
        return f"{obj.product.name} - {attribute_values_str}"

class AttributeAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    search_fields = ('name',)

class AttributeValueAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    search_fields = ('attribute_value',)

def _register(model, admin_class):
    admin.site.register(model, admin_class)

_register(models.Category, CategoryAdmin)
_register(models.Sub_Category, Sub_CategoryAdmin)
_register(models.Product, ProductAdmin)
_register(models.ProductLine, ProductLineAdmin)
_register(models.Attribute, AttributeAdmin)
_register(models.AttributeValue, AttributeValueAdmin)

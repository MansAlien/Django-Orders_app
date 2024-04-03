from import_export.admin import ImportExportModelAdmin
# vim: set fileencoding=utf-8 :
from django.contrib import admin
import orders.models as models


class CategoryAdmin(ImportExportModelAdmin, admin.ModelAdmin):

    list_display = ('id', 'name')
    list_filter = ('id', 'name')
    search_fields = ('name',)


class Sub_CategoryAdmin(ImportExportModelAdmin, admin.ModelAdmin):

    list_display = ('id', 'category', 'name')
    list_filter = ('category', 'id', 'name')
    search_fields = ('name',)


def _register(model, admin_class):
    admin.site.register(model, admin_class)


_register(models.Category, CategoryAdmin)
_register(models.Sub_Category, Sub_CategoryAdmin)

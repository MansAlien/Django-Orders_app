from django.contrib import admin
from .models import Category, Sub_Category


class CategoryAdmin(admin.ModelAdmin):
  list_display = ("id", "name",)

class SubCategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "category")
  
admin.site.register(Category, CategoryAdmin)
admin.site.register(Sub_Category, SubCategoryAdmin)

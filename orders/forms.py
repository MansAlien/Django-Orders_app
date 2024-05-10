
from django import forms
from orders.models import Category, Sub_Category


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'is_active']

class SubCategoryForm(forms.ModelForm):
    class Meta:
        model = Sub_Category
        fields = ['category', 'name', 'is_active']


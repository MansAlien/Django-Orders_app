
from django import forms
from orders.models import Category, Sub_Category, Attribute, Product, ProductLine, AttributeValue


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'is_active']

class SubCategoryForm(forms.ModelForm):
    class Meta:
        model = Sub_Category
        fields = ['category', 'name', 'is_active']

class AttributeForm(forms.ModelForm):
    class Meta:
        model = Attribute
        fields = ['name', 'description']

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['sub_category', 'name', 'description', 'is_active', 'is_countable']

class AttributeValueForm(forms.ModelForm):
    class Meta:
        model = AttributeValue
        fields = ['product', 'attribute', 'attribute_value']

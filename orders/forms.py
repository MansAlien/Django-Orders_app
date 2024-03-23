
from django import forms
from orders.models import Category, Sub_Category

class Sub_Category_Form(forms.Form):
    category = forms.ModelChoiceField(queryset=Category.objects.all())

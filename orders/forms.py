
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

class ProductLineForm(forms.ModelForm):
    class Meta:
        model = ProductLine
        fields = ['product', 'attribute_values', 'normal_price', 'stock_qty', 'min_stock_qty', 'is_active']

class ProductLineCreateForm(forms.Form):
    product = forms.ModelChoiceField(queryset=Product.objects.all(),
        widget=forms.Select(attrs={"hx-get":"load_product_values/", "hx-target":"#id_attribute_values"}))
    attribute_values = forms.ModelMultipleChoiceField(queryset=AttributeValue.objects.none())
    normal_price = forms.DecimalField(decimal_places=2, max_digits=10)
    fawry_price = forms.DecimalField(decimal_places=2, max_digits=10)
    stock_qty = forms.IntegerField(initial=0)
    min_stock_qty = forms.IntegerField(initial=1)
    is_active = forms.BooleanField()
    admin_comment = forms.CharField(widget=forms.Textarea(attrs={"rows": 3}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if "product" in self.data:
            product_id = int(self.data.get("product"))
            self.fields["attribute_values"].queryset =AttributeValue.objects.filter(product=product_id) 


    def clean_stock_qty(self):
        stock_qty = self.cleaned_data['stock_qty']
        if stock_qty < 0:
            raise forms.ValidationError("Stock quantity cannot be negative.")
        return stock_qty

    def save(self):
        product_line = ProductLine(
            product=self.cleaned_data['product'],
            normal_price=self.cleaned_data['normal_price'],
            fawry_price=self.cleaned_data['fawry_price'],
            stock_qty=self.cleaned_data['stock_qty'],
            min_stock_qty=self.cleaned_data['min_stock_qty'],
            is_active=self.cleaned_data['is_active']
        )
        product_line.save()
        product_line.attribute_values.set(self.cleaned_data['attribute_values'])
        return product_line


from django import forms
from orders.models import Category, Sub_Category, Attribute, Product, ProductLine, AttributeValue, Customer, OrderDetail
from django.forms import widgets


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
        widgets = { "description":forms.Textarea(attrs={"rows": 3}) }

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['sub_category', 'name', 'description', 'is_active', 'is_countable']
        widgets = { "description":forms.Textarea(attrs={"rows": 3}) }

class AttributeValueForm(forms.ModelForm):
    class Meta:
        model = AttributeValue
        fields = ['product', 'attribute', 'attribute_value']

class ProductLineForm(forms.ModelForm):
    class Meta:
        model = ProductLine
        fields = ['product', 'attribute_values', 'normal_price', 'fawry_price', 'stock_qty', 'admin_comment', 'min_stock_qty','deliver_date', 'is_active']
        widgets = { "description":forms.Textarea(attrs={"rows": 3}) }

class ProductLineCreateForm(forms.Form):
    product = forms.ModelChoiceField(queryset=Product.objects.all(),
        widget=forms.Select(attrs={"hx-get":"load_product_values/", "hx-target":"#id_attribute_values"}))
    attribute_values = forms.ModelMultipleChoiceField(
        queryset=AttributeValue.objects.none(),
        widget=forms.SelectMultiple(attrs={"size": 3})  # Adjust the size as needed
    )
    normal_price = forms.DecimalField(decimal_places=2, max_digits=10)
    fawry_price = forms.DecimalField(decimal_places=2, max_digits=10)
    admin_comment = forms.CharField(required=False, widget=forms.Textarea(attrs={"rows": 3}))
    stock_qty = forms.IntegerField(initial=0)
    min_stock_qty = forms.IntegerField(initial=1)
    deliver_date = forms.IntegerField()
    is_active = forms.BooleanField()

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

class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['phone', 'name_one', 'name_two', 'whatsapp']

class OrderDetailForm(forms.ModelForm):
    location = forms.CharField(required=False,
        widget=widgets.TextInput(attrs={
            'class': 'bg-gray-700 rounded-lg w-96 text-white py-1 px-2',
            'placeholder': 'location',
            'x-show': 'input',  # Add your custom attributes here
            ':id':"$id('location')",
            '_': 'on keyup put my value into the next <span/>',
        })
    )
    customer_comment = forms.CharField(required=False,
        widget=widgets.TextInput(attrs={
            'class': 'bg-gray-700 rounded-lg w-96 text-white py-1 px-2',
            'placeholder': 'comment',
            'x-show': 'input',  # Add your custom attributes here
            ':id':"$id('comment')",
            '_': 'on keyup put my value into the next <span/>',
        }))
    amount = forms.CharField(
        widget=widgets.TextInput(attrs={
            'class': 'flex-shrink-0 text-white border-0 bg-transparent text-sm font-normal focus:outline-none focus:ring-0 w-[2rem] text-center',
            'value': '1',
            '_': """
                    on change set me.closest('tr').querySelector('.total-price').innerText to
                    ((parseInt(me.closest('tr').querySelector('.price').innerText) * parseInt(me.value)).toFixed(2))
                    then call calculateTotal()
                 """,
        }))
    deliver_type = forms.ChoiceField(
        choices=[('N', 'normal'), ('F', 'fawry')],
        widget=widgets.Select(attrs={
            'class': 'border text-sm rounded-full block p-1 bg-gray-700 border-gray-600 placeholder-gray-400 text-white focus:ring-blue-500 focus:border-blue-500',
            '_': """
                    on change if my.value == 'F' then 
                    set me.closest('tr').querySelector('.price').innerText to {{ product_line.fawry_price }} 
                    then set me.closest('tr').querySelector('.total-price').innerText to 
                    ({{ product_line.fawry_price }} * parseInt(me.closest('tr').querySelector('input[type=text]').value)).toFixed(2) 
                    then call calculateTotal()
                    else 
                    set me.closest('tr').querySelector('.price').innerText to {{ product_line.normal_price }} 
                    then set me.closest('tr').querySelector('.total-price').innerText to 
                    ({{ product_line.normal_price }} * parseInt(me.closest('tr').querySelector('input[type=text]').value)).toFixed(2)
                    then call calculateTotal()
                """,
        })) 
    delivery_Status = forms.ChoiceField(
        choices=[('P', 'Printing'), ('D', 'Delivered')],
        widget=widgets.Select(attrs={
            'class': 'border text-sm rounded-full block p-1 bg-gray-700 border-gray-600 placeholder-gray-400 text-white focus:ring-blue-500 focus:border-blue-500',
        })) 
    deliver_date = forms.DateField(
        widget=widgets.DateInput(attrs={
            'class': 'bg-gray-700 rounded-lg w-96 text-white py-1 px-2',
            'type': 'date',
            'value': '2024-06-16',
            'data-value': '2024-06-16T12:00Z',
            'x-data': "{date: new Date($el.dataset.value)}",
            ':value': "date.toLocaleDateString('sv-en')",
            '_': "on change put my value into the next .date",
            ':id' : "$id('date')",
            'x-show':"input",
        }))
    deliver_time = forms.TimeField(
        widget=widgets.TimeInput(attrs={
            'class': 'bg-gray-700 rounded-lg text-white py-1 px-2',
            'type': 'time',
            'value': '12:00:00',
            'data-value': '2024-06-16T12:00Z',
            'x-data': "{date: new Date($el.dataset.value)}",
            ':value': "date.toLocaleTimeString('sv-en')",
            '_': "on change put my value into the next .time",
            ':id' : "$id('time')",
            'x-show':"input",
        }))
    class Meta:
        model = OrderDetail
        fields = ['product_line', 'deliver_type', 'delivery_Status', 'amount', 'customer_comment', 'location', 'deliver_date', 'deliver_time']

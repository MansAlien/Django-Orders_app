from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    is_active = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.name

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.sub_category_set.update(is_active=self.is_active)

        for sub_category in self.sub_category_set.all():
            sub_category.product_set.update(is_active=self.is_active)

            for product in sub_category.product_set.all():
                product.productline_set.update(is_active=self.is_active)
                    


class Sub_Category(models.Model):
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    name = models.CharField(max_length=200, unique=True)
    is_active = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.name

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.product_set.update(is_active=self.is_active)

        for product in self.product_set.all():
            product.productline_set.update(is_active=self.is_active)

class Attribute(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(null=True, blank=True)

    def __str__(self) -> str:
        return self.name

class Product(models.Model):
    sub_category = models.ForeignKey(Sub_Category, on_delete=models.PROTECT)
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(null=True, blank=True)
    is_active = models.BooleanField(default=False)
    is_countable = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)

    def __str__(self) -> str:
        return self.name

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.productline_set.update(is_active=self.is_active)

class AttributeValue(models.Model):
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    attribute = models.ForeignKey(Attribute, on_delete=models.CASCADE)
    attribute_value = models.CharField(max_length=100)

    def __str__(self) -> str:
        return f"{self.attribute.name} : {self.attribute_value}"

class ProductLine(models.Model):
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    attribute_values = models.ManyToManyField(AttributeValue, related_name="attribute_values")
    normal_price = models.DecimalField(decimal_places=2, max_digits=10)
    fawry_price = models.DecimalField(decimal_places=2, max_digits=10)
    stock_qty = models.IntegerField(default=0)
    min_stock_qty = models.IntegerField(default=1)
    is_active = models.BooleanField(default=False)
    deliver_date = models.IntegerField(null=True)
    admin_comment = models.TextField(null=True, blank=True)

    def save(self, *args, **kwargs):
        if self.stock_qty == 0 and self.product.is_countable:
            self.is_active = False
        super().save(*args, **kwargs)

    def values(self):
        attribute_values_str = ', '.join(str(attr_value.attribute_value) for attr_value in self.attribute_values.all())
        return attribute_values_str

    def __str__(self):
        attribute_values_str = ', '.join(str(attr_value) for attr_value in self.attribute_values.all())
        return f"{self.product.name} - {attribute_values_str}"


class Customer(models.Model):
    name_one = models.CharField(max_length=100)
    name_two = models.CharField(max_length=100, blank=True, null=True)
    phone = models.CharField(max_length=12, unique=True)
    whatsapp = models.CharField(max_length=12, unique=True)

    def __str__(self) -> str:
        return f"{self.name_one} ({self.name_two})"


class Order(models.Model):
    STATUS = {
        "P":"Printing",
        "D":"Delivered",
    }
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT)
    delivery_status = models.CharField(max_length=1, choices=STATUS, default="P")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)

    def __str__(self) -> str:
        return f"{self.customer} --> ({self.get_delivery_status_display()})"


class OrderDetail(models.Model):
    DELIVER_TYPE = {
        "N":"Normal",
        "F":"Fawry",
    }
    STATUS = {
        "P":"Printing",
        "D":"Delivered",
    }
    order = models.ForeignKey(Order, on_delete=models.PROTECT)
    product_line = models.ForeignKey(ProductLine, on_delete=models.PROTECT)
    deliver_type = models.CharField(max_length=1, choices=DELIVER_TYPE, default="N")
    delivery_Status = models.CharField(max_length=1, choices=STATUS, default="P")
    is_active = models.BooleanField(default=True)
    amount = models.PositiveIntegerField(default=1)
    customer_comment = models.TextField(null=True, blank=True)
    location = models.CharField(max_length=200, null=True, blank=True)
    created_at = models.DateTimeField(null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, editable=False)
    deliver_date = models.DateField(null=True, blank=True)
    deliver_time = models.TimeField(null=True, blank=True)

    def __str__(self) -> str:
        return f"{self.product_line}"

class Payment(models.Model):
    PAYMENT_METHOD = {
        "C":"Cash",
        "O":"Online",
        "V":"Visa",
    }
    order = models.ForeignKey(Order, on_delete=models.PROTECT)
    discount = models.DecimalField(decimal_places=1, max_digits=4, null=True, blank=True, default=0.00)
    total = models.DecimalField(decimal_places=2, max_digits=10, null=True, blank=True)
    paid = models.DecimalField(decimal_places=2, max_digits=10, null=True, blank=True, default=0.00)
    payment_method = models.CharField(max_length=1, choices=PAYMENT_METHOD, default="C")

    def __str__(self) -> str:
        return f"Total:{self.total}- Paid:{self.paid}"

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT, null=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.content

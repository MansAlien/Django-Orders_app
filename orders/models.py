from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    is_active = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.name

class Sub_Category(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    is_active = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.name

class Attribute(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)

    def __str__(self) -> str:
        return self.name

class Product(models.Model):
    sub_category = models.ForeignKey(Sub_Category, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(null=True, blank=True)
    is_active = models.BooleanField(default=False)
    is_countable = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)

    def __str__(self) -> str:
        return self.name

class AttributeValue(models.Model):
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    attribute = models.ForeignKey(Attribute, on_delete=models.CASCADE)
    attribute_value = models.CharField(max_length=100)

    def __str__(self) -> str:
        return f"{self.attribute.name} : {self.attribute_value}"

class ProductLine(models.Model):
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    attribute_values = models.ManyToManyField(AttributeValue, related_name="attribute_values")
    price = models.DecimalField(decimal_places=2, max_digits=5)
    stock_qty = models.IntegerField(default=0)
    min_stock_qty = models.IntegerField(default=1)
    is_active = models.BooleanField(default=False)

    def __str__(self):
        attribute_values_str = ', '.join(str(attr_value) for attr_value in self.attribute_values.all())
        return f"{self.product.name} - {attribute_values_str}"


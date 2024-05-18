# Generated by Django 5.0.2 on 2024-05-18 09:12

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("orders", "0004_alter_attribute_name_alter_product_sub_category_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="Customer",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("first_name", models.CharField(max_length=100)),
                ("last_name", models.CharField(max_length=100)),
                ("phone", models.CharField(max_length=12)),
                ("whatsapp", models.CharField(max_length=12)),
                (
                    "gender",
                    models.CharField(
                        choices=[("M", "Male"), ("F", "Female")],
                        default="M",
                        max_length=1,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Order",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("delivered", models.BooleanField(default=False)),
                ("is_active", models.BooleanField(default=False)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                (
                    "customer",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        to="orders.customer",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Comment",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("content", models.TextField()),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                (
                    "customer",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="orders.customer",
                    ),
                ),
                (
                    "order",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="orders.order"
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="OrderDetail",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "deliver_type",
                    models.CharField(
                        choices=[("N", "Normal"), ("F", "Fawry")],
                        default="N",
                        max_length=1,
                    ),
                ),
                ("delivered", models.BooleanField(default=False)),
                ("is_active", models.BooleanField(default=False)),
                ("amount", models.PositiveIntegerField(default=1)),
                ("customer_comment", models.TextField(blank=True, null=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "order",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT, to="orders.order"
                    ),
                ),
                (
                    "product_line",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        to="orders.productline",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Payment",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("discount", models.DecimalField(decimal_places=1, max_digits=4)),
                ("total", models.DecimalField(decimal_places=2, max_digits=10)),
                ("paid", models.DecimalField(decimal_places=2, max_digits=10)),
                (
                    "order",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT, to="orders.order"
                    ),
                ),
            ],
        ),
    ]

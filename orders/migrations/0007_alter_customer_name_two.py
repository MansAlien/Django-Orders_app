# Generated by Django 5.0.2 on 2024-06-01 07:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("orders", "0006_alter_customer_whatsapp"),
    ]

    operations = [
        migrations.AlterField(
            model_name="customer",
            name="name_two",
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]

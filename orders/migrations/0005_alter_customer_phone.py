# Generated by Django 5.0.2 on 2024-05-29 06:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("orders", "0004_rename_discription_attribute_description_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="customer",
            name="phone",
            field=models.CharField(max_length=12, unique=True),
        ),
    ]

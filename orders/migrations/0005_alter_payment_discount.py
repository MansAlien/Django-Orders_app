# Generated by Django 5.0.2 on 2024-06-13 19:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0004_alter_payment_discount_alter_payment_paid_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payment',
            name='discount',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=4),
        ),
    ]

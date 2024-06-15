# Generated by Django 5.0.2 on 2024-06-13 20:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0006_alter_payment_discount'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payment',
            name='paid',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=10, null=True),
        ),
    ]
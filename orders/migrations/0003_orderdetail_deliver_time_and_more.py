# Generated by Django 5.0.2 on 2024-06-10 23:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0002_alter_payment_discount_alter_payment_paid'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderdetail',
            name='deliver_time',
            field=models.TimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='orderdetail',
            name='deliver_date',
            field=models.DateField(blank=True, null=True),
        ),
    ]
# Generated by Django 5.0.2 on 2024-05-02 09:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0008_loggedinuser"),
    ]

    operations = [
        migrations.DeleteModel(
            name="LoggedInUser",
        ),
    ]

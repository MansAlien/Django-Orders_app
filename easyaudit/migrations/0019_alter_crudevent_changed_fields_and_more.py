# Generated by Django 5.0.1 on 2024-03-18 19:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('easyaudit', '0018_rename_crudevent_object_id_content_type_index'),
    ]

    operations = [
        migrations.AlterField(
            model_name='crudevent',
            name='changed_fields',
            field=models.TextField(blank=True, default='', verbose_name='Changed fields'),
        ),
        migrations.AlterField(
            model_name='crudevent',
            name='object_json_repr',
            field=models.TextField(blank=True, default='', verbose_name='Object JSON representation'),
        ),
        migrations.AlterField(
            model_name='crudevent',
            name='object_repr',
            field=models.TextField(blank=True, default='', verbose_name='Object representation'),
        ),
        migrations.AlterField(
            model_name='crudevent',
            name='user_pk_as_string',
            field=models.CharField(blank=True, default='', help_text='String version of the user pk', max_length=255, verbose_name='User PK as string'),
        ),
        migrations.AlterField(
            model_name='loginevent',
            name='remote_ip',
            field=models.CharField(db_index=True, default='', max_length=50, verbose_name='Remote IP'),
        ),
        migrations.AlterField(
            model_name='loginevent',
            name='username',
            field=models.CharField(blank=True, default='', max_length=255, verbose_name='Username'),
        ),
        migrations.AlterField(
            model_name='requestevent',
            name='query_string',
            field=models.TextField(default='', verbose_name='Query string'),
        ),
        migrations.AlterField(
            model_name='requestevent',
            name='remote_ip',
            field=models.CharField(db_index=True, default='', max_length=50, verbose_name='Remote IP'),
        ),
    ]

# Generated by Django 4.1.13 on 2024-06-23 18:05

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0030_sheetfilter_querysets_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='sheetfilter_querysets',
            name='columns',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='sheetfilter_querysets',
            name='rows',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='account_activation',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2024, 6, 23, 23, 35, 18, 683596)),
        ),
        migrations.AlterField(
            model_name='account_activation',
            name='expiry_date',
            field=models.DateTimeField(default=datetime.datetime(2024, 6, 25, 23, 35, 18, 682598)),
        ),
        migrations.AlterField(
            model_name='chartfilters',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2024, 6, 23, 23, 35, 18, 685594)),
        ),
        migrations.AlterField(
            model_name='dashboard_data',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2024, 6, 23, 23, 35, 18, 687594)),
        ),
        migrations.AlterField(
            model_name='datasource_querysets',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2024, 6, 23, 23, 35, 18, 685594)),
        ),
        migrations.AlterField(
            model_name='datasourcefilter',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2024, 6, 23, 23, 35, 18, 685594)),
        ),
        migrations.AlterField(
            model_name='filedetails',
            name='uploaded_at',
            field=models.DateTimeField(default=datetime.datetime(2024, 6, 23, 23, 35, 18, 684596)),
        ),
        migrations.AlterField(
            model_name='functions_tb',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2024, 6, 23, 23, 35, 18, 686594)),
        ),
        migrations.AlterField(
            model_name='license_key',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2024, 6, 23, 23, 35, 18, 686594)),
        ),
        migrations.AlterField(
            model_name='querysets',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2024, 6, 23, 23, 35, 18, 685594)),
        ),
        migrations.AlterField(
            model_name='reset_password',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2024, 6, 23, 23, 35, 18, 683596)),
        ),
        migrations.AlterField(
            model_name='serverdetails',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2024, 6, 23, 23, 35, 18, 684596)),
        ),
        migrations.AlterField(
            model_name='sheet_data',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2024, 6, 23, 23, 35, 18, 686594)),
        ),
        migrations.AlterField(
            model_name='sheetfilter_querysets',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2024, 6, 23, 23, 35, 18, 687594)),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2024, 6, 23, 23, 35, 18, 681596)),
        ),
    ]

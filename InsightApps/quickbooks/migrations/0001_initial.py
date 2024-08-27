# Generated by Django 4.1.13 on 2024-07-24 13:27

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='TokenStoring',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.IntegerField(blank=True, db_column='user_id', null=True)),
                ('qbuserid', models.CharField(blank=True, db_column='Quickbooks_user_id', max_length=1000, null=True)),
                ('tokentype', models.CharField(blank=True, db_column='token_type', max_length=100, null=True)),
                ('accesstoken', models.CharField(blank=True, db_column='access_token', max_length=1800, null=True)),
                ('refreshtoken', models.CharField(blank=True, db_column='refresh_token', max_length=1800, null=True)),
                ('idtoken', models.CharField(blank=True, db_column='id_token', max_length=1800, null=True)),
                ('realm_id', models.CharField(blank=True, db_column='realm_id', max_length=100, null=True)),
                ('created_at', models.DateTimeField(default=datetime.datetime(2024, 7, 24, 18, 57, 42, 514587))),
                ('updated_at', models.DateTimeField(default=datetime.datetime(2024, 7, 24, 18, 57, 42, 514587))),
                ('expiry_date', models.DateTimeField(default=datetime.datetime(2024, 7, 24, 19, 57, 42, 514587))),
            ],
            options={
                'db_table': 'quickbooks_token',
            },
        ),
    ]

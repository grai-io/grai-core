# Generated by Django 4.2 on 2023-04-26 12:21

import django_multitenant.models
from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("notifications", "0001_initial"),
    ]

    operations = [
        migrations.AlterModelManagers(
            name="alert",
            managers=[
                ("objects", django_multitenant.models.TenantManager()),
            ],
        ),
    ]

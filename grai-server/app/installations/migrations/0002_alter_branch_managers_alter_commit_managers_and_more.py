# Generated by Django 4.1.7 on 2023-04-03 15:01

import django_multitenant.models
from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("installations", "0001_initial"),
    ]

    operations = [
        migrations.AlterModelManagers(
            name="branch",
            managers=[
                ("objects", django_multitenant.models.TenantManager()),
            ],
        ),
        migrations.AlterModelManagers(
            name="commit",
            managers=[
                ("objects", django_multitenant.models.TenantManager()),
            ],
        ),
        migrations.AlterModelManagers(
            name="pullrequest",
            managers=[
                ("objects", django_multitenant.models.TenantManager()),
            ],
        ),
        migrations.AlterModelManagers(
            name="repository",
            managers=[
                ("objects", django_multitenant.models.TenantManager()),
            ],
        ),
    ]

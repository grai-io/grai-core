# Generated by Django 4.1.5 on 2023-01-30 09:43

import uuid

import connections.models
import django.db.models.deletion
import django_multitenant.fields
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("connections", "0006_alter_connector_name"),
    ]

    operations = [
        migrations.AddField(
            model_name="run",
            name="connector",
            field=models.ForeignKey(
                default="768aea48-1146-4f14-9005-40e89504f4b3",
                on_delete=django.db.models.deletion.PROTECT,
                related_name="runs",
                to="connections.connector",
            ),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="run",
            name="connection",
            field=django_multitenant.fields.TenantForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="runs",
                to="connections.connection",
            ),
        ),
        migrations.CreateModel(
            name="RunFile",
            fields=[
                ("id", models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ("file", models.FileField(editable=False, upload_to=connections.models.directory_path)),
                ("name", models.CharField(editable=False, max_length=255)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "run",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, related_name="files", to="connections.run"
                    ),
                ),
            ],
        ),
    ]

# Generated by Django 4.2.1 on 2023-05-30 15:09

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("connections", "0020_connector_events_alter_run_action"),
    ]

    operations = [
        migrations.AlterField(
            model_name="run",
            name="connection",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, related_name="runs", to="connections.connection"
            ),
        ),
    ]

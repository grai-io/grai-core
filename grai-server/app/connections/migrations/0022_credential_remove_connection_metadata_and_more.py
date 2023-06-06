# Generated by Django 4.2.1 on 2023-05-30 15:17

from django.db import migrations, models
import django_multitenant.mixins
import django_multitenant.models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):
    dependencies = [
        ("connections", "0021_alter_run_connection"),
        ("lineage", "0009_source_source_source_name_uniqueness"),
        ("workspaces", "0006_workspace_workspaces__name_5adeb1_idx"),
    ]

    operations = [
        migrations.AddField(
            model_name="connection",
            name="source",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                related_name="connections",
                to="lineage.source",
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="run",
            name="source",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                related_name="runs",
                to="lineage.source",
            ),
            preserve_default=False,
        ),
    ]

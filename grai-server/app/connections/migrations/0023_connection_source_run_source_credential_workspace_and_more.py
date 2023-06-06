# Generated by Django 4.2.1 on 2023-05-30 15:17

from django.db import migrations, models
import django.db.models.deletion
from lineage.models import Source


def create_sources(apps, schema_editor):
    # We can't import the Person model directly as it may be a newer
    # version than this migration expects. We use the historical version.
    Connection = apps.get_model("connections", "Connection")

    for connection in Connection.objects.all():
        source, created = Source.objects.get_or_create(
            workspace_id=connection.workspace_id,
            name=connection.connector.slug,
        )

        connection.source_id = source.id
        connection.save()


def add_source_to_run(apps, schema_editor):
    # We can't import the Person model directly as it may be a newer
    # version than this migration expects. We use the historical version.
    from connections.models import Run

    for run in Run.objects.all():
        run.source_id = run.connection.source_id
        run.save()


class Migration(migrations.Migration):
    dependencies = [
        ("connections", "0022_credential_remove_connection_metadata_and_more"),
    ]

    operations = [
        migrations.RunPython(create_sources),
        migrations.RunPython(add_source_to_run),
    ]

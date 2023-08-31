# Generated by Django 4.2.4 on 2023-08-31 18:17

from django.db import migrations, models
import grai_schemas.serializers


class Migration(migrations.Migration):
    dependencies = [
        ("lineage", "0015_source_intermediate_tables"),
    ]

    operations = [
        migrations.AlterField(
            model_name="edge",
            name="metadata",
            field=models.JSONField(
                default=dict, encoder=grai_schemas.serializers.GraiEncoder
            ),
        ),
        migrations.AlterField(
            model_name="node",
            name="metadata",
            field=models.JSONField(
                default=dict, encoder=grai_schemas.serializers.GraiEncoder
            ),
        ),
    ]

# Generated by Django 4.0.6 on 2022-08-02 02:40

import uuid

import django.db.models.deletion
import django.db.models.expressions
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Edge",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("name", models.CharField(max_length=255)),
                ("namespace", models.CharField(default="default", max_length=255)),
                ("display_name", models.CharField(max_length=255)),
                ("data_source", models.CharField(max_length=255)),
                ("metadata", models.JSONField(default=dict)),
                ("is_active", models.BooleanField(default=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name="Node",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("namespace", models.CharField(default="default", max_length=255)),
                ("name", models.CharField(max_length=255)),
                ("display_name", models.CharField(max_length=255)),
                ("data_source", models.CharField(max_length=255)),
                ("metadata", models.JSONField(default=dict)),
                ("is_active", models.BooleanField(default=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.AddIndex(
            model_name="node",
            index=models.Index(fields=["namespace", "name"], name="lineage_nod_namespa_742536_idx"),
        ),
        migrations.AddConstraint(
            model_name="node",
            constraint=models.UniqueConstraint(fields=("namespace", "name"), name="Node namespaces/name uniqueness"),
        ),
        migrations.AddField(
            model_name="edge",
            name="destination",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT,
                related_name="destination_edge",
                to="lineage.node",
            ),
        ),
        migrations.AddField(
            model_name="edge",
            name="source",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT,
                related_name="source_edge",
                to="lineage.node",
            ),
        ),
        migrations.AddIndex(
            model_name="edge",
            index=models.Index(fields=["is_active"], name="lineage_edg_is_acti_1522cd_idx"),
        ),
        migrations.AddIndex(
            model_name="edge",
            index=models.Index(fields=["namespace", "name"], name="lineage_edg_namespa_f8f692_idx"),
        ),
        migrations.AddConstraint(
            model_name="edge",
            constraint=models.CheckConstraint(
                check=models.Q(
                    ("source", django.db.models.expressions.F("destination")),
                    _negated=True,
                ),
                name="Edges are not allowed between the same nodes",
            ),
        ),
        migrations.AddConstraint(
            model_name="edge",
            constraint=models.UniqueConstraint(fields=("namespace", "name"), name="Edge namespaces/name uniqueness"),
        ),
        migrations.AddConstraint(
            model_name="edge",
            constraint=models.UniqueConstraint(
                condition=models.Q(("is_active", True)),
                fields=("source", "destination"),
                name="one_active_edge_between_nodes",
            ),
        ),
    ]

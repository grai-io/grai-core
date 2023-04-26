# Generated by Django 4.2 on 2023-04-26 12:21

import uuid

import django.db.models.deletion
import django_multitenant.mixins
import django_multitenant.models
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        (
            "workspaces",
            "0004_alter_membership_managers_alter_workspace_managers_and_more",
        ),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("lineage", "0004_alter_edge_managers_alter_node_managers"),
    ]

    operations = [
        migrations.CreateModel(
            name="Filter",
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
                ("name", models.CharField(blank=True, max_length=255, null=True)),
                ("metadata", models.JSONField(default=dict)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "created_by",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="filters",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "workspace",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="filters",
                        to="workspaces.workspace",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
            bases=(django_multitenant.mixins.TenantModelMixin, models.Model),
            managers=[
                ("objects", django_multitenant.models.TenantManager()),
            ],
        ),
    ]

# Generated by Django 4.1.5 on 2023-01-15 14:21

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ("workspaces", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Organisation",
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
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.RemoveIndex(
            model_name="workspace",
            name="workspaces__name_5adeb1_idx",
        ),
        migrations.AddField(
            model_name="workspace",
            name="organisation",
            field=models.ForeignKey(
                default="0cec206a-57e0-4534-aa78-ba726a7e8f54",
                on_delete=django.db.models.deletion.CASCADE,
                related_name="workspaces",
                to="workspaces.organisation",
            ),
            preserve_default=False,
        ),
        migrations.AddIndex(
            model_name="workspace",
            index=models.Index(
                fields=["organisation", "name"], name="workspaces__organis_007202_idx"
            ),
        ),
        migrations.AddConstraint(
            model_name="workspace",
            constraint=models.UniqueConstraint(
                fields=("organisation", "name"),
                name="Organisation workspace name uniqueness",
            ),
        ),
        migrations.AddIndex(
            model_name="organisation",
            index=models.Index(fields=["name"], name="workspaces__name_fedc67_idx"),
        ),
        migrations.AddConstraint(
            model_name="organisation",
            constraint=models.UniqueConstraint(
                fields=("name",), name="Organisation name uniqueness"
            ),
        ),
    ]

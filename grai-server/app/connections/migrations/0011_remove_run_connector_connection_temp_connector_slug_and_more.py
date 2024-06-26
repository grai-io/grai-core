# Generated by Django 4.1.7 on 2023-02-15 12:39

import uuid

from django.db import migrations, models
from django_multitenant.mixins import TenantModelMixin


def monkey_patch_multitenant() -> None:
    def __setattr__(self, attrname, val):
        if (
            attrname in ("tenant_id", "tenant")
            and not self._state.adding
            and val
            and self.tenant_value
            and val != self.tenant_value
            and val != self.tenant_object
        ):
            self._try_update_tenant = True

        return super(TenantModelMixin, self).__setattr__(attrname, val)

    TenantModelMixin.__setattr__ = __setattr__

    @property
    def tenant_field(self):
        return "tenant_id"

    TenantModelMixin.tenant_field = tenant_field

    @property
    def tenant_value(self):
        return self.tenant_id

    TenantModelMixin.tenant_value = tenant_value

    @property
    def tenant_object(self):
        return self.tenant

    TenantModelMixin.tenant_object = tenant_object


def forwards_func(apps, schema_editor):
    old_field = TenantModelMixin.tenant_field
    old_value = TenantModelMixin.tenant_value
    old_object = TenantModelMixin.tenant_object
    monkey_patch_multitenant()

    # We get the model from the versioned app registry;
    # if we directly import it, it'll be the wrong version
    Run = apps.get_model("connections", "Run")
    Connection = apps.get_model("connections", "Connection")
    db_alias = schema_editor.connection.alias
    runs = Run.objects.using(db_alias).filter(connection_id=None).all()

    for run in runs:
        connection_name = f"{run.connector.name} {uuid.uuid4()}"

        connection = Connection.objects.using(db_alias).create(
            workspace=run.workspace,
            connector=run.connector,
            name=connection_name,
            is_active=True,
            temp=True,
        )
        run.connection = connection
        run.save()

    TenantModelMixin.tenant_field = old_field
    TenantModelMixin.tenant_value = old_value
    TenantModelMixin.tenant_object = old_object


class Migration(migrations.Migration):
    dependencies = [
        ("connections", "0010_alter_connector_name"),
    ]

    operations = [
        migrations.AddField(
            model_name="connection",
            name="temp",
            field=models.BooleanField(default=False),
        ),
        migrations.RunPython(forwards_func),
        migrations.RemoveField(
            model_name="run",
            name="connector",
        ),
        migrations.AddField(
            model_name="connector",
            name="slug",
            field=models.CharField(
                blank=True,
                choices=[
                    ("postgres", "postgres"),
                    ("snowflake", "snowflake"),
                    ("dbt", "dbt"),
                    ("yaml_file", "yaml_file"),
                    ("mssql", "mssql"),
                    ("bigquery", "bigquery"),
                    ("fivetran", "fivetran"),
                ],
                max_length=255,
                null=True,
            ),
        ),
        migrations.AddField(
            model_name="run",
            name="action",
            field=models.CharField(
                choices=[("tests", "tests"), ("update", "update")], default="update", max_length=255
            ),
        ),
    ]

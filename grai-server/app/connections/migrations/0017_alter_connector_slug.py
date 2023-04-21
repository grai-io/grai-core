# Generated by Django 4.1.7 on 2023-04-21 14:14

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("connections", "0016_alter_connection_managers_alter_run_managers"),
    ]

    operations = [
        migrations.AlterField(
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
                    ("mysql", "mysql"),
                    ("redshift", "redshift"),
                ],
                max_length=255,
                null=True,
            ),
        ),
    ]

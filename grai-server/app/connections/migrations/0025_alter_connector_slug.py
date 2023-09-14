# Generated by Django 4.2.4 on 2023-08-04 13:14

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("connections", "0024_alter_connection_source_alter_run_source"),
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
                    ("dbt_cloud", "dbt_cloud"),
                    ("yaml_file", "yaml_file"),
                    ("mssql", "mssql"),
                    ("bigquery", "bigquery"),
                    ("fivetran", "fivetran"),
                    ("mysql", "mysql"),
                    ("redshift", "redshift"),
                    ("metabase", "metabase"),
                    ("looker", "looker"),
                ],
                max_length=255,
                null=True,
            ),
        ),
    ]

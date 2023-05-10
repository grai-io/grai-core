# Generated by Django 4.2 on 2023-05-10 09:55

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("connections", "0018_remove_connection_node_namespaces_name_uniqueness_connection_and_more"),
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
                ],
                max_length=255,
                null=True,
            ),
        ),
    ]

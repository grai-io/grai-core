# Generated by Django 4.1.6 on 2023-02-08 10:46

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("connections", "0008_alter_connector_name"),
    ]

    operations = [
        migrations.AlterField(
            model_name="connector",
            name="name",
            field=models.CharField(
                choices=[
                    ("PostgreSQL", "PostgreSQL"),
                    ("Snowflake", "Snowflake"),
                    ("dbt", "dbt"),
                    ("YAML File", "YAML File"),
                    ("Microsoft SQL Server", "Microsoft SQL Server"),
                    ("Google BigQuery", "Google BigQuery"),
                ],
                max_length=255,
            ),
        ),
    ]

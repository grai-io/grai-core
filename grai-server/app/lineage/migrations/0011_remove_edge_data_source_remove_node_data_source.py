# Generated by Django 4.2.2 on 2023-06-16 16:41

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("lineage", "0010_remove_edge_data_source_remove_node_data_source_and_more"),
        ("connections", "0023_connection_source_run_source_alter_run_connection"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="edge",
            name="data_source",
        ),
        migrations.RemoveField(
            model_name="node",
            name="data_source",
        ),
    ]

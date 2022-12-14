# Generated by Django 4.1.4 on 2022-12-14 17:29

from django.db import migrations
import django.db.models.deletion
import django_multitenant.fields


class Migration(migrations.Migration):

    dependencies = [
        ("lineage", "0003_edge_workspace_node_workspace"),
    ]

    operations = [
        migrations.AlterField(
            model_name="edge",
            name="destination",
            field=django_multitenant.fields.TenantForeignKey(
                on_delete=django.db.models.deletion.PROTECT,
                related_name="destination_edges",
                to="lineage.node",
            ),
        ),
        migrations.AlterField(
            model_name="edge",
            name="source",
            field=django_multitenant.fields.TenantForeignKey(
                on_delete=django.db.models.deletion.PROTECT,
                related_name="source_edges",
                to="lineage.node",
            ),
        ),
    ]

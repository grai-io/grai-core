# Generated by Django 4.2.6 on 2023-10-31 17:27

from django.db import migrations, models
import django.db.models.deletion
import pgvector.django


class Migration(migrations.Migration):
    dependencies = [
        ("lineage", "0017_invalid_source_lineage_state"),
    ]

    operations = [
        pgvector.django.VectorExtension(),
        migrations.CreateModel(
            name="NodeEmbeddings",
            fields=[
                ("embedding", pgvector.django.VectorField(dimensions=1536)),
                (
                    "node",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        primary_key=True,
                        serialize=False,
                        to="lineage.node",
                    ),
                ),
            ],
            options={
                "indexes": [
                    pgvector.django.HnswIndex(
                        ef_construction=128,
                        fields=["embedding"],
                        m=64,
                        name="node_embedding_index",
                        opclasses=["vector_ip_ops"],
                    )
                ],
            },
        ),
    ]
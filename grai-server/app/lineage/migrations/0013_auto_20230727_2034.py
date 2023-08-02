# Generated by Django 4.2.3 on 2023-07-27 20:34

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("lineage", "0012_alter_edge_display_name_alter_edge_name_and_more"),
    ]

    operations = [
        migrations.RunSQL(
            sql="""
              ALTER TABLE lineage_node ADD COLUMN search tsvector GENERATED ALWAYS AS (
                setweight(to_tsvector('simple', coalesce(replace(replace(name, '_', '\_'), '.', '\.'), '')) , 'A') ||
                setweight(to_tsvector('simple', coalesce(replace(replace(namespace, '_', '\_'), '.', '\.'), '')), 'B')
              ) STORED;
            """,
            reverse_sql="""
              ALTER TABLE lineage_node DROP COLUMN search;
            """,
        ),
        migrations.RunSQL(
            sql="""
                CREATE INDEX IF NOT EXISTS textsearch_idx ON lineage_node USING GIN (search);
            """,
            reverse_sql="""
                DROP INDEX IF EXISTS textsearch_idx;
            """,
        ),
        migrations.RunSQL(
            sql="""
              CREATE MATERIALIZED VIEW IF NOT EXISTS unique_lexeme AS SELECT word FROM ts_stat('SELECT search FROM lineage_node')
            """,
            reverse_sql="""
              DROP MATERIALIZED VIEW IF EXISTS unique_lexeme;
            """,
        ),
        migrations.RunSQL(
            sql="""
              CREATE EXTENSION IF NOT EXISTS fuzzystrmatch;
            """,
            reverse_sql="",
        ),
    ]

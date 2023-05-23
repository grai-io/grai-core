import redis

from django.core.management.base import BaseCommand, CommandError, CommandParser

from workspaces.models import Workspace


class Command(BaseCommand):
    help = "Build the lineage cache"

    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument("workspace_id", type=str)

        parser.add_argument(
            "--delete",
            action="store_true",
        )

    def handle(self, *args, **options) -> None:
        workspace_id = options["workspace_id"]
        try:
            self.workspace = Workspace.objects.get(pk=workspace_id)
        except Workspace.DoesNotExist:
            raise CommandError('workspace "%s" does not exist' % workspace_id)

        if options["delete"]:
            self.clear_cache()

        self.build_cache()

        self.stdout.write(self.style.SUCCESS('Successfully built cache for workspace "%s"' % self.workspace.name))

    def build_cache(self):
        def escape_string(input: str):
            return input.replace("'", "\\'")

        r = redis.Redis(host="localhost", port=6379, db=0)

        for node in self.workspace.nodes.all():
            node_type = node.metadata["grai"]["node_type"]
            node_name = escape_string(node.name)

            if node_type == "Table":
                node_namespace = escape_string(node.namespace)
                node_data_source = escape_string(node.data_source)

                r.graph(f"lineage:{str(self.workspace.id)}").query(
                    f"MERGE (table:Table {{id: '{str(node.id)}'}}) ON CREATE SET table.name = '{node_name}', table.namespace = '{node_namespace}', table.data_source = '{node_data_source}' ON MATCH SET table.name = '{node_name}', table.namespace = '{node_namespace}', table.data_source = '{node_data_source}'"
                )

            elif node_type == "Column":
                r.graph(f"lineage:{str(self.workspace.id)}").query(
                    f"MERGE (column:Column {{id: '{str(node.id)}'}}) ON CREATE SET column.name = '{node_name}' ON MATCH SET column.name = '{node_name}'"
                )

        for edge in self.workspace.edges.all():
            edge_type = edge.metadata["grai"]["edge_type"]

            if edge_type == "TableToColumn":
                r.graph(f"lineage:{str(self.workspace.id)}").query(
                    f"MATCH (table:Table), (column:Column) WHERE table.id = '{str(edge.source_id)}' AND column.id = '{str(edge.destination_id)}' MERGE (table)-[r:TABLE_TO_COLUMN]->(column)"
                )
            elif edge_type == "TableToTable":
                r.graph(f"lineage:{str(self.workspace.id)}").query(
                    f"MATCH (source:Table), (destination:Table) WHERE source.id = '{str(edge.source_id)}' AND destination.id = '{str(edge.destination_id)}' MERGE (source)-[r:TABLE_TO_TABLE]->(destination)"
                )
            elif edge_type == "ColumnToColumn":
                r.graph(f"lineage:{str(self.workspace.id)}").query(
                    f"MATCH (source:Column), (destination:Column) WHERE source.id = '{str(edge.source_id)}' AND destination.id = '{str(edge.destination_id)}' MERGE (source)-[r:COLUMN_TO_COLUMN]->(destination)"
                )

                source_table_edge = edge.source.destination_edges.filter(
                    metadata__grai__edge_type="TableToColumn"
                ).first()
                destination_table_edge = edge.destination.destination_edges.filter(
                    metadata__grai__edge_type="TableToColumn"
                ).first()

                r.graph(f"lineage:{str(self.workspace.id)}").query(
                    f"MATCH (source:Table), (destination:Table) WHERE source.id = '{str(source_table_edge.source_id)}' AND destination.id = '{str(destination_table_edge.source_id)}' MERGE (source)-[r:TABLE_TO_TABLE_COPY]->(destination)"
                )

    def clear_cache(self):
        r = redis.Redis(host="localhost", port=6379, db=0)
        r.delete(f"lineage:{str(self.workspace.id)}")

        self.stdout.write(self.style.SUCCESS('Successfully cleared cache for workspace "%s"' % self.workspace.name))

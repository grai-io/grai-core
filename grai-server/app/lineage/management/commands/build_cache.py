import redis

from django.core.management.base import BaseCommand, CommandError, CommandParser

from workspaces.models import Workspace


class Command(BaseCommand):
    help = "Build the lineage cache"

    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument("workspace_id", type=str)

    def handle(self, *args, **options) -> None:
        workspace_id = options["workspace_id"]
        try:
            self.workspace = Workspace.objects.get(pk=workspace_id)
        except Workspace.DoesNotExist:
            raise CommandError('workspace "%s" does not exist' % workspace_id)

        self.build_cache()

        self.stdout.write(self.style.SUCCESS('Successfully built cache for workspace "%s"' % self.workspace.name))

    def build_cache(self):
        r = redis.Redis(host="localhost", port=6379, db=0)

        for node in self.workspace.nodes.all():
            node_type = node.metadata["grai"]["node_type"]

            if node_type == "Table":
                r.graph(f"lineage:{str(self.workspace.id)}").query(
                    f"MERGE (table:Table {{id: '{str(node.id)}'}}) ON CREATE SET table.name = '{node.name}', table.namespace = '{node.namespace}' ON MATCH SET table.name = '{node.name}', table.namespace = '{node.namespace}'"
                )

            elif node_type == "Column":
                r.graph(f"lineage:{str(self.workspace.id)}").query(
                    f"MERGE (column:Column {{id: '{str(node.id)}'}}) ON CREATE SET column.name = '{node.name}' ON MATCH SET column.name = '{node.name}'"
                )

        for edge in self.workspace.edges.all():
            edge_type = edge.metadata["grai"]["edge_type"]

            if edge_type == "TableToColumn":
                r.graph(f"lineage:{str(self.workspace.id)}").query(
                    f"MATCH (table:Table), (column:Column) WHERE table.id = '{str(edge.source_id)}' AND column.id = '{str(edge.destination_id)}' MERGE (table)-[r:TABLE_TO_COLUMN]->(column)"
                )
            elif edge_type == "TableToTable":
                r.graph(f"lineage:{str(self.workspace.id)}").query(
                    f"MATCH (source:Table), (destination:Table) WHERE source.id = '{str(edge.source_id)}' AND destination.id = '{str(edge.destination_id)}' MERGE (source)-[r:TABLE_TO_TABLE]->(destination) ON CREATE SET r.temp = False ON MATCH SET r.temp = False"
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
                    f"MATCH (source:Table), (destination:Table) WHERE source.id = '{str(source_table_edge.source_id)}' AND destination.id = '{str(destination_table_edge.source_id)}' MERGE (source)-[r:TABLE_TO_TABLE]->(destination) ON CREATE SET r.temp = True"
                )

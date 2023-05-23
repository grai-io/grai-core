import redis
from django.core.management.base import CommandError, CommandParser
from django_multitenant.utils import set_current_tenant
from django_tqdm import BaseCommand
from query_chunk import chunk

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

            set_current_tenant(self.workspace)

        except Workspace.DoesNotExist:
            raise CommandError('workspace "%s" does not exist' % workspace_id)

        self.redis_connection = redis.Redis(host="localhost", port=6379, db=0)

        if options["delete"]:
            self.clear_cache()

        self.build_cache()

        self.stdout.write(self.style.SUCCESS('Successfully built cache for workspace "%s"' % self.workspace.name))

    def build_cache(self):
        node_tqdm = self.tqdm(total=self.workspace.nodes.count())

        for node in chunk(self.workspace.nodes.all(), 10000):
            node_type = node.metadata["grai"]["node_type"]

            if node_type == "Table":
                self.redis_connection.graph(f"lineage:{str(self.workspace.id)}").query(
                    f"""
                        MERGE (table:Table {{id: $id}})
                        ON CREATE SET table.name = $name, table.namespace = $namespace, table.data_source = $data_source
                        ON MATCH SET table.name = $name, table.namespace = $namespace, table.data_source = $data_source
                    """,
                    {
                        "id": str(node.id),
                        "name": node.name,
                        "namespace": node.namespace,
                        "data_source": node.data_source,
                    },
                )

            elif node_type == "Column":
                self.redis_connection.graph(f"lineage:{str(self.workspace.id)}").query(
                    f"""
                        MERGE (column:Column {{id: $id}})
                        ON CREATE SET column.name = $name
                        ON MATCH SET column.name = $name
                    """,
                    {
                        "id": str(node.id),
                        "name": node.name,
                    },
                )

            node_tqdm.update(1)

        edge_tqdm = self.tqdm(total=self.workspace.edges.count())

        for edge in chunk(self.workspace.edges.all(), 10000):
            edge_type = edge.metadata["grai"]["edge_type"]

            if edge_type == "TableToColumn":
                self.redis_connection.graph(f"lineage:{str(self.workspace.id)}").query(
                    f"""
                        MATCH (table:Table), (column:Column)
                        WHERE table.id = $source
                        AND column.id = $destination
                        MERGE (table)-[r:TABLE_TO_COLUMN]->(column)
                    """,
                    {
                        "source": str(edge.source_id),
                        "destination": str(edge.destination_id),
                    },
                )
            elif edge_type == "TableToTable":
                self.redis_connection.graph(f"lineage:{str(self.workspace.id)}").query(
                    f"""
                        MATCH (source:Table), (destination:Table)
                        WHERE source.id = $source
                        AND destination.id = $destination
                        MERGE (source)-[r:TABLE_TO_TABLE]->(destination)
                    """,
                    {
                        "source": str(edge.source_id),
                        "destination": str(edge.destination_id),
                    },
                )
            elif edge_type == "ColumnToColumn":
                self.redis_connection.graph(f"lineage:{str(self.workspace.id)}").query(
                    f"""
                        MATCH (source:Column), (destination:Column)
                        WHERE source.id = $source
                        AND destination.id = $destination
                        MERGE (source)-[r:COLUMN_TO_COLUMN]->(destination)
                    """,
                    {
                        "source": str(edge.source_id),
                        "destination": str(edge.destination_id),
                    },
                )

                source_table_edge = edge.source.destination_edges.filter(
                    metadata__grai__edge_type="TableToColumn"
                ).first()
                destination_table_edge = edge.destination.destination_edges.filter(
                    metadata__grai__edge_type="TableToColumn"
                ).first()

                self.redis_connection.graph(f"lineage:{str(self.workspace.id)}").query(
                    f"MATCH (source:Table), (destination:Table) WHERE source.id = '{str(source_table_edge.source_id)}' AND destination.id = '{str(destination_table_edge.source_id)}' MERGE (source)-[r:TABLE_TO_TABLE_COPY]->(destination)"
                )

            edge_tqdm.update(1)

    def clear_cache(self):
        self.redis_connection.delete(f"lineage:{str(self.workspace.id)}")

        self.stdout.write(self.style.SUCCESS('Successfully cleared cache for workspace "%s"' % self.workspace.name))

import redis
from redis import Redis

from workspaces.models import Workspace


class GraphCache:
    manager: Redis
    workspace: Workspace

    def __init__(self, workspace: Workspace):
        self.workspace = workspace

        self.manager = redis.Redis(host="localhost", port=6379, db=0)

    def clear_cache(self):
        self.manager.delete(f"lineage:{str(self.workspace.id)}")

    def cache_node(self, node):
        node_type = node.metadata["grai"]["node_type"]

        if node_type == "Table":
            self.manager.graph(f"lineage:{str(self.workspace.id)}").query(
                """
                    MERGE (table:Table {id: $id})
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
            self.manager.graph(f"lineage:{str(self.workspace.id)}").query(
                """
                    MERGE (column:Column {id: $id})
                    ON CREATE SET column.name = $name
                    ON MATCH SET column.name = $name
                """,
                {
                    "id": str(node.id),
                    "name": node.name,
                },
            )

    def cache_edge(self, edge):
        edge_type = edge.metadata["grai"]["edge_type"]

        if edge_type == "TableToColumn":
            self.manager.graph(f"lineage:{str(self.workspace.id)}").query(
                """
                    MATCH (table:Table), (column:Column)
                    WHERE table.id = $source
                    AND column.id = $destination
                    MERGE (table)-[r:TABLE_TO_COLUMN {id: $id}]->(column)
                """,
                {
                    "id": str(edge.id),
                    "source": str(edge.source_id),
                    "destination": str(edge.destination_id),
                },
            )
        elif edge_type == "TableToTable":
            self.manager.graph(f"lineage:{str(self.workspace.id)}").query(
                """
                    MATCH (source:Table), (destination:Table)
                    WHERE source.id = $source
                    AND destination.id = $destination
                    MERGE (source)-[r:TABLE_TO_TABLE {id: $id}]->(destination)
                """,
                {
                    "id": str(edge.id),
                    "source": str(edge.source_id),
                    "destination": str(edge.destination_id),
                },
            )
        elif edge_type == "ColumnToColumn":
            self.manager.graph(f"lineage:{str(self.workspace.id)}").query(
                """
                    MATCH (source:Column), (destination:Column)
                    WHERE source.id = $source
                    AND destination.id = $destination
                    MERGE (source)-[r:COLUMN_TO_COLUMN {id: $id}]->(destination)
                """,
                {
                    "id": str(edge.id),
                    "source": str(edge.source_id),
                    "destination": str(edge.destination_id),
                },
            )

            source_table_edge = edge.source.destination_edges.filter(metadata__grai__edge_type="TableToColumn").first()
            destination_table_edge = edge.destination.destination_edges.filter(
                metadata__grai__edge_type="TableToColumn"
            ).first()

            self.manager.graph(f"lineage:{str(self.workspace.id)}").query(
                """
                  MATCH (source:Table), (destination:Table)
                  WHERE source.id = $source
                  AND destination.id = $destination
                  MERGE (source)-[r:TABLE_TO_TABLE_COPY]->(destination)
                """,
                {
                    "source": str(source_table_edge.source_id),
                    "destination": str(destination_table_edge.source_id),
                },
            )

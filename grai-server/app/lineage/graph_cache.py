from typing import List, Optional

import redis
from django.conf import settings
from redis import Redis

from workspaces.models import Workspace

from .graph_types import GraphColumn, GraphTable
from query_chunk import chunk


class GraphCache:
    manager: Redis
    workspace: Workspace

    def __init__(self, workspace: Workspace):
        self.workspace = workspace

        self.manager = redis.Redis(
            host=settings.REDIS_GRAPH_CACHE_HOST,
            port=settings.REDIS_GRAPH_CACHE_PORT,
            db=0,
        )

    def query(self, query: str, parameters: any = {}, timeout: int = None):
        return self.manager.graph(f"lineage:{str(self.workspace.id)}").query(query, parameters, timeout=timeout)

    def build_cache(self):
        for node in chunk(self.workspace.nodes.all(), 10000):
            self.cache_node(node)

        for edge in chunk(self.workspace.edges.all(), 10000):
            self.cache_edge(edge)

    def clear_cache(self):
        self.manager.delete(f"lineage:{str(self.workspace.id)}")

    def cache_node(self, node):
        def get_data_source() -> Optional[str]:
            source = node.data_sources.first()

            if not source:
                return None

            connection = source.connections.first()

            if connection:
                return f"grai-source-{connection.connector.slug}"

            return source.name

        node_type = node.metadata.get("grai", {}).get("node_type")

        if node_type == "Table":
            self.query(
                """
                    MERGE (table:Table {id: $id})
                    ON CREATE SET table.name = $name, table.display_name = $display_name, table.namespace = $namespace, table.data_source = $data_source, table.tags = $tags
                    ON MATCH SET table.name = $name, table.display_name = $display_name, table.namespace = $namespace, table.data_source = $data_source, table.tags = $tags
                """,
                {
                    "id": str(node.id),
                    "name": node.name,
                    "display_name": node.display_name,
                    "namespace": node.namespace,
                    "data_source": get_data_source(),
                    "tags": node.metadata.get("grai", {}).get("tags"),
                },
            )

        elif node_type == "Column":
            self.query(
                """
                    MERGE (column:Column {id: $id})
                    ON CREATE SET column.name = $name, column.display_name = $display_name
                    ON MATCH SET column.name = $name, column.display_name = $display_name
                """,
                {
                    "id": str(node.id),
                    "name": node.name,
                    "display_name": node.display_name,
                },
            )

    def delete_node(self, node):
        self.query(
            """
                MATCH (n {id: $id})
                DELETE n
            """,
            {
                "id": str(node.id),
            },
        )

    def cache_edge(self, edge):
        edge_type = edge.metadata.get("grai", {}).get("edge_type")

        if edge_type == "TableToColumn":
            self.query(
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
            self.query(
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
            self.query(
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

            if not source_table_edge or not destination_table_edge:
                return

            self.query(
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

    def delete_edge(self, edge):
        self.query(
            """
                MATCH ()-[r {id: $id}]-()
                DELETE r
            """,
            {
                "id": str(edge.id),
            },
        )

    def get_graph_result(self, where: str = "") -> List[GraphTable]:
        result = self.query(
            f"""
                MATCH (table:Table)
                {where}
                OPTIONAL MATCH (table:Table)-[:TABLE_TO_COLUMN]->(column:Column)
                OPTIONAL MATCH (column)-[:COLUMN_TO_COLUMN]->(column_destination:Column)
                OPTIONAL MATCH (table)-[:TABLE_TO_TABLE]->(destination:Table)
                WITH
                    table,
                    COLLECT(distinct destination.id) AS destinations,
                    column,
                    collect(distinct column_destination.id) as column_destinations
                WITH
                    table,
                    destinations,
                    collect({{
                        id: column.id,
                        name: column.name,
                        display_name: column.display_name,
                        column_destinations: column_destinations
                    }}) AS columns
                WITH
                    table,
                    {{
                        id: table.id,
                        name: table.name,
                        display_name: table.display_name,
                        namespace: table.namespace,
                        data_source: table.data_source,
                        columns: columns,
                        destinations: destinations
                    }} AS tables
                RETURN tables
            """,
            timeout=10000,
        )

        tables = []

        for node in result.result_set:
            table = node[0]

            columns = [
                GraphColumn(
                    id=column.get("id"),
                    name=column.get("name"),
                    display_name=column.get("display_name"),
                    sources=[],
                    destinations=column.get("column_destinations", []),
                )
                for column in table.get("columns")
                if column.get("id")
            ]

            tables.append(
                GraphTable(
                    id=table.get("id"),
                    name=table.get("name"),
                    display_name=table.get("display_name"),
                    namespace=table.get("namespace"),
                    data_source=table.get("data_source"),
                    columns=columns,
                    sources=[],
                    destinations=table.get("destinations", []),
                    table_destinations=[],
                    table_sources=[],
                )
            )

        return tables

    def get_filtered_graph_result(self, filter):
        if len(filter.metadata) == 0:
            return self.get_graph_result()

        match = []
        where = []

        for row in filter.metadata:
            value = row["value"]

            if row["type"] == "table":
                if row["field"] == "tag":
                    if row["operator"] == "contains":
                        where.append(f"'{value}' IN table.tags")
            elif row["type"] == "ancestor":
                if row["field"] == "tag":
                    if row["operator"] == "contains":
                        match.append("MATCH (table)<-[:TABLE_TO_TABLE|:TABLE_TO_TABLE_COPY*]-(othertable:Table)")
                        where.append(f"'{value}' IN othertable.tags")
            elif row["type"] == "no-ancestor":
                if row["field"] == "tag":
                    if row["operator"] == "contains":
                        # where.append(f"(table)<-[:TABLE_TO_TABLE|:TABLE_TO_TABLE_COPY*]-(othertable:Table) AND '{value}' IN othertable.tags")
                        pass
            elif row["type"] == "descendant":
                if row["field"] == "tag":
                    if row["operator"] == "contains":
                        match.append("MATCH (table)-[:TABLE_TO_TABLE|:TABLE_TO_TABLE_COPY*]->(othertable:Table)")
                        where.append(f"'{value}' IN othertable.tags")
            elif row["type"] == "no-descendant":
                if row["field"] == "tag":
                    if row["operator"] == "contains":
                        # where.append(f"(table)-[:TABLE_TO_TABLE|:TABLE_TO_TABLE_COPY*]->(othertable:Table) AND '{value}' IN othertable.tags")
                        pass
            else:
                raise Exception("Unknown filter type: " + row["type"])

        where_clause = f"{' '.join(match)} WHERE ({') AND ('.join(where)})"

        return self.get_graph_result(where=where_clause)

    def get_with_step_graph_result(self, n: int, parameters: any = {}, where: str = None) -> List["GraphTable"]:
        result = self.query(
            f"""
                MATCH (firsttable:Table)
                {where}
                OPTIONAL MATCH (firsttable:Table)-[:TABLE_TO_TABLE|:TABLE_TO_TABLE_COPY*0..{n}]-(table:Table)
                OPTIONAL MATCH (table:Table)-[:TABLE_TO_TABLE|:TABLE_TO_TABLE_COPY]->(table_destinations:Table)
                OPTIONAL MATCH (table_sources:Table)-[:TABLE_TO_TABLE|:TABLE_TO_TABLE_COPY]->(table:Table)
                OPTIONAL MATCH (table:Table)-[:TABLE_TO_COLUMN]->(column:Column)
                OPTIONAL MATCH (column)-[:COLUMN_TO_COLUMN]->(column_destination:Column)
                OPTIONAL MATCH (table)-[:TABLE_TO_TABLE]->(destination:Table)
                WITH
                    table,
                    COLLECT(distinct destination.id) AS destinations,
                    column,
                    collect(distinct column_destination.id) as column_destinations,
                    collect(distinct table_destinations.id) as table_destinations,
                    collect(distinct table_sources.id) as table_sources
                WITH
                    table,
                    destinations,
                    table_destinations,
                    table_sources,
                    collect({{
                        id: column.id,
                        name: column.name,
                        display_name: column.display_name,
                        column_destinations: column_destinations
                    }}) AS columns
                WITH
                    table,
                    {{
                        id: table.id,
                        name: table.name,
                        display_name: table.display_name,
                        namespace: table.namespace,
                        data_source: table.data_source,
                        columns: columns,
                        destinations: destinations,
                        table_destinations: table_destinations,
                        table_sources: table_sources
                    }} AS tables
                RETURN tables
            """,
            parameters,
            timeout=10000,
        )

        tables = []

        for node in result.result_set:
            table = node[0]

            columns = [
                GraphColumn(
                    id=column.get("id"),
                    name=column.get("name"),
                    display_name=column.get("display_name"),
                    sources=[],
                    destinations=column.get("column_destinations"),
                )
                for column in table.get("columns")
                if column.get("id")
            ]

            tables.append(
                GraphTable(
                    id=table.get("id"),
                    name=table.get("name"),
                    display_name=table.get("display_name"),
                    namespace=table.get("namespace"),
                    data_source=table.get("data_source"),
                    columns=columns,
                    sources=[],
                    destinations=table.get("destinations"),
                    table_destinations=table.get("table_destinations"),
                    table_sources=table.get("table_sources"),
                )
            )

        return tables

    def get_table_filtered_graph_result(self, table_id: str, n: int) -> List["GraphTable"]:
        parameters = {"table": table_id}
        where = "WHERE firsttable.id = $table"

        return self.get_with_step_graph_result(n, parameters, where)

    def get_edge_filtered_graph_result(self, edge_id: str, n: int = 1) -> List["GraphTable"]:
        parameters = {"edge": edge_id}
        where = """
            WHERE (
                ()-[{id: $edge}]-(firsttable:Table) OR
                ()-[{id: $edge}]-(:Column)-[:TABLE_TO_COLUMN]-(firsttable:Table)
            )
        """

        return self.get_with_step_graph_result(n, parameters, where)

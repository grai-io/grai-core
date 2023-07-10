import uuid
from typing import List, Optional, Union

import redis
from django.conf import settings
from grandalf.graphs import Edge, Graph, Vertex
from grandalf.layouts import SugiyamaLayout
from redis import Redis

from workspaces.models import Workspace

from .graph import GraphQuery
from .graph_types import BaseGraph, GraphColumn, GraphTable


class GraphCache:
    manager: Redis
    workspace_id: str

    def __init__(self, workspace: Union[Workspace, str]):
        self.workspace_id = (
            workspace if isinstance(workspace, str) or isinstance(workspace, uuid.UUID) else str(workspace.id)
        )

        self.manager = redis.Redis(
            host=settings.REDIS_GRAPH_CACHE_HOST,
            port=settings.REDIS_GRAPH_CACHE_PORT,
            db=0,
        )

    def query(self, query: str, parameters: object = {}, timeout: int = None):
        return self.manager.graph(f"lineage:{str(self.workspace_id)}").query(query, parameters, timeout=timeout)

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

        if node_type in ["Table", "Query"]:
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

    def update_node(self, id: str, x: int, y: int):
        self.query(
            """
                MATCH (n {id: $id})
                SET n.x = $x, n.y = $y
            """,
            {
                "id": id,
                "x": x,
                "y": y,
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

    def get_table_ids(self):
        results = self.query(
            """
                MATCH (n:Table)
                WITH
                    n.id as ids
                RETURN ids
            """
        ).result_set

        return [result[0] for result in results]

    def get_tables(self, search: Optional[str] = None):
        query = f"""
            MATCH (table:Table)
            {f"WHERE toLower(table.name) CONTAINS toLower('{search}')" if search else ""}
            WITH
                table,
                {{
                    id: table.id,
                    name: table.name,
                    display_name: table.display_name,
                    namespace: table.namespace,
                    data_source: table.data_source,
                    x: table.x,
                    y: table.y
                }} AS tables
            RETURN tables
            LIMIT 100
        """

        results = self.query(query).result_set

        return [BaseGraph(**result[0]) for result in results]

    def get_table_edges(self):
        results = self.query(
            """
                MATCH (source:Table)-[r:TABLE_TO_TABLE|:TABLE_TO_TABLE_COPY]->(destination:Table)
                WITH
                    r,
                    {
                        id: r.id,
                        source_id: source.id,
                        destination_id: destination.id
                    } AS edges
                RETURN edges
            """
        ).result_set

        return [result[0] for result in results]

    def get_graph_result(
        self,
        query: GraphQuery,
    ) -> List[GraphTable]:
        query.add(
            f"""
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
                        x: table.x,
                        y: table.y,
                        columns: columns,
                        destinations: destinations
                    }} AS tables
                RETURN tables
            """
        )

        result = self.query(str(query), query.get_parameters(), timeout=10000)

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
                    x=table.get("x"),
                    y=table.get("y"),
                    columns=columns,
                    sources=[],
                    destinations=table.get("destinations", []),
                    table_destinations=[],
                    table_sources=[],
                )
            )

        return tables

    def filter_by_range(self, min_x: int, max_x: int, min_y: int, max_y: int, query: GraphQuery) -> GraphQuery:
        query.match(
            "(table)-[:TABLE_TO_TABLE|:TABLE_TO_TABLE_COPY*0..1]-(d)",
            where=[
                "$min_x <= d.x <= $max_x",
                "$min_y <= d.y <= $max_y",
            ],
            parameters={
                "min_x": min_x,
                "max_x": max_x,
                "min_y": min_y,
                "max_y": max_y,
            },
        )

        return query

    def filter_by_filters(self, filters, query: GraphQuery) -> GraphQuery:
        for filter in filters:
            query = self.filter_by_filter(filter, query)

    def filter_by_filter(self, filter, query: GraphQuery) -> GraphQuery:
        if len(filter.metadata) == 0:
            return query

        for row in filter.metadata:
            value = row["value"]

            if row["type"] == "table":
                if row["field"] == "tag":
                    if row["operator"] == "contains":
                        query.where(f"'{value}' IN table.tags")
            elif row["type"] == "ancestor":
                if row["field"] == "tag":
                    if row["operator"] == "contains":
                        query.match(
                            "(table)<-[:TABLE_TO_TABLE|:TABLE_TO_TABLE_COPY*]-(othertable:Table)",
                            where=f"'{value}' IN othertable.tags",
                        )
            elif row["type"] == "no-ancestor":
                if row["field"] == "tag":
                    if row["operator"] == "contains":
                        # where.append(f"(table)<-[:TABLE_TO_TABLE|:TABLE_TO_TABLE_COPY*]-(othertable:Table) AND '{value}' IN othertable.tags")
                        pass
            elif row["type"] == "descendant":
                if row["field"] == "tag":
                    if row["operator"] == "contains":
                        query.match(
                            "(table)-[:TABLE_TO_TABLE|:TABLE_TO_TABLE_COPY*]->(othertable:Table)",
                            where=f"'{value}' IN othertable.tags",
                        )
            elif row["type"] == "no-descendant":
                if row["field"] == "tag":
                    if row["operator"] == "contains":
                        # where.append(f"(table)-[:TABLE_TO_TABLE|:TABLE_TO_TABLE_COPY*]->(othertable:Table) AND '{value}' IN othertable.tags")
                        pass
            else:
                raise Exception("Unknown filter type: " + row["type"])

        return query

    def get_with_step_graph_result(
        self, n: int, parameters: object = {}, where: Optional[str] = None
    ) -> List["GraphTable"]:
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
                        x: table.x,
                        y: table.y,
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
                    x=table.get("x"),
                    y=table.get("y"),
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

    def layout_graph(self):
        table_ids = self.get_table_ids()
        edges = self.get_table_edges()

        vertexes = {}

        class defaultview(object):
            w, h = 200, 400

        for table_id in table_ids:
            vertexes[table_id] = Vertex(table_id)

        V = list(vertexes.values())

        for v in V:
            v.view = defaultview()

        E = [Edge(vertexes[edge["source_id"]], vertexes[edge["destination_id"]]) for edge in edges]

        g = Graph(V, E)

        graphs = []
        single_tables = []

        for graph in g.C:
            if len(graph.sV) == 1:
                node = graph.sV[0]

                single_tables.append(node)
                continue

            sug = SugiyamaLayout(graph)
            sug.init_all()
            sug.draw(20)

            minX = 0
            maxX = 0
            # minY = 0
            # maxY = 0

            for vertex in graph.sV:
                minX = min(minX, vertex.view.xy[1])
                maxX = max(maxX, vertex.view.xy[1])
                # minY = min(minY, vertex.view.xy[0])
                # maxY = max(maxY, vertex.view.xy[0])

            graphs.append(
                {
                    "minX": minX,
                    "maxX": maxX,
                    # "minY": minY,
                    # "maxY": maxY,
                    "nodes": graph.sV,
                }
            )

        x = 0
        y = 0

        for graph in graphs:
            for v in graph["nodes"]:
                self.update_node(v.data, v.view.xy[1] + x + graph["minX"], v.view.xy[0])

            x += graph["maxX"] - graph["minX"] + 400

        start_x = x
        index = 0

        for table in single_tables:
            self.update_node(table.data, x, y)

            if index > 20:
                y += 200
                x = start_x
                index = 0
                continue

            x += 500
            index += 1

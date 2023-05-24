from typing import List

import redis

from .types import GraphColumn, GraphTable


def get_graph_result(workspace_id: str) -> List["GraphTable"]:
    r = redis.Redis(host="localhost", port=6379, db=0)

    result = r.graph(f"lineage:{str(workspace_id)}").query(
        f"""
MATCH (table:Table)
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
        column_destinations: column_destinations
    }}) AS columns
WITH
    table,
    {{
        id: table.id,
        name: table.name,
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
                namespace=table.get("namespace"),
                data_source=table.get("data_source"),
                columns=columns,
                sources=[],
                destinations=table.get("destinations", []),
            )
        )

    return tables


def get_filtered_graph_result(workspace_id: str, table_id: str, n: int) -> List["GraphTable"]:
    r = redis.Redis(host="localhost", port=6379, db=0)

    result = r.graph(f"lineage:{str(workspace_id)}").query(
        f"""
            MATCH (firsttable:Table {{id: $table}})
            OPTIONAL MATCH (firsttable:Table)-[:TABLE_TO_TABLE|:TABLE_TO_TABLE_COPY*0..{n}]-(table:Table)
            OPTIONAL MATCH (table:Table)-[:TABLE_TO_TABLE|:TABLE_TO_TABLE_COPY]->(all_destinations:Table)
            OPTIONAL MATCH (all_sources:Table)-[:TABLE_TO_TABLE|:TABLE_TO_TABLE_COPY]->(table:Table)
            OPTIONAL MATCH (table:Table)-[:TABLE_TO_COLUMN]->(column:Column)
            OPTIONAL MATCH (column)-[:COLUMN_TO_COLUMN]->(column_destination:Column)
            OPTIONAL MATCH (table)-[:TABLE_TO_TABLE]->(destination:Table)
            WITH
                table,
                COLLECT(distinct destination.id) AS destinations,
                column,
                collect(distinct column_destination.id) as column_destinations,
                collect(distinct all_destinations.id) as all_destinations,
                collect(distinct all_sources.id) as all_sources
            WITH
                table,
                destinations,
                all_destinations,
                all_sources,
                collect({{
                    id: column.id,
                    name: column.name,
                    column_destinations: column_destinations
                }}) AS columns
            WITH
                table,
                {{
                    id: table.id,
                    name: table.name,
                    namespace: table.namespace,
                    data_source: table.data_source,
                    columns: columns,
                    destinations: destinations,
                    all_destinations: all_destinations,
                    all_sources: all_sources
                }} AS tables
            RETURN tables
        """,
        {
            "table": table_id,
        },
        timeout=10000,
    )

    tables = []

    for node in result.result_set:
        table = node[0]

        columns = [
            GraphColumn(
                id=column.get("id"),
                name=column.get("name"),
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
                namespace=table.get("namespace"),
                data_source=table.get("data_source"),
                columns=columns,
                sources=[],
                destinations=table.get("destinations"),
                all_destinations=table.get("all_destinations"),
                all_sources=table.get("all_sources"),
            )
        )

    return tables


def get_edge_filtered_graph_result(workspace_id: str, edge_id: str, n: int = 1) -> List["GraphTable"]:
    r = redis.Redis(host="localhost", port=6379, db=0)

    result = r.graph(f"lineage:{str(workspace_id)}").query(
        f"""
            MATCH ()-[{{id: $edge}}]-(firsttable:Table)
            OPTIONAL MATCH (firsttable:Table)-[:TABLE_TO_TABLE|:TABLE_TO_TABLE_COPY*0..{n}]-(table:Table)
            OPTIONAL MATCH (table:Table)-[:TABLE_TO_TABLE|:TABLE_TO_TABLE_COPY]->(all_destinations:Table)
            OPTIONAL MATCH (all_sources:Table)-[:TABLE_TO_TABLE|:TABLE_TO_TABLE_COPY]->(table:Table)
            OPTIONAL MATCH (table:Table)-[:TABLE_TO_COLUMN]->(column:Column)
            OPTIONAL MATCH (column)-[:COLUMN_TO_COLUMN]->(column_destination:Column)
            OPTIONAL MATCH (table)-[:TABLE_TO_TABLE]->(destination:Table)
            WITH
                table,
                COLLECT(distinct destination.id) AS destinations,
                column,
                collect(distinct column_destination.id) as column_destinations,
                collect(distinct all_destinations.id) as all_destinations,
                collect(distinct all_sources.id) as all_sources
            WITH
                table,
                destinations,
                all_destinations,
                all_sources,
                collect({{
                    id: column.id,
                    name: column.name,
                    column_destinations: column_destinations
                }}) AS columns
            WITH
                table,
                {{
                    id: table.id,
                    name: table.name,
                    namespace: table.namespace,
                    data_source: table.data_source,
                    columns: columns,
                    destinations: destinations,
                    all_destinations: all_destinations,
                    all_sources: all_sources
                }} AS tables
            RETURN tables
            UNION
            MATCH ()-[{{id: $edge}}]-(:Column)-[:TABLE_TO_COLUMN]-(firsttable:Table)
            OPTIONAL MATCH (firsttable:Table)-[:TABLE_TO_TABLE|:TABLE_TO_TABLE_COPY*0..{n}]-(table:Table)
            OPTIONAL MATCH (table:Table)-[:TABLE_TO_TABLE|:TABLE_TO_TABLE_COPY]->(all_destinations:Table)
            OPTIONAL MATCH (all_sources:Table)-[:TABLE_TO_TABLE|:TABLE_TO_TABLE_COPY]->(table:Table)
            OPTIONAL MATCH (table:Table)-[:TABLE_TO_COLUMN]->(column:Column)
            OPTIONAL MATCH (column)-[:COLUMN_TO_COLUMN]->(column_destination:Column)
            OPTIONAL MATCH (table)-[:TABLE_TO_TABLE]->(destination:Table)
            WITH
                table,
                COLLECT(distinct destination.id) AS destinations,
                column,
                collect(distinct column_destination.id) as column_destinations,
                collect(distinct all_destinations.id) as all_destinations,
                collect(distinct all_sources.id) as all_sources
            WITH
                table,
                destinations,
                all_destinations,
                all_sources,
                collect({{
                    id: column.id,
                    name: column.name,
                    column_destinations: column_destinations
                }}) AS columns
            WITH
                table,
                {{
                    id: table.id,
                    name: table.name,
                    namespace: table.namespace,
                    data_source: table.data_source,
                    columns: columns,
                    destinations: destinations,
                    all_destinations: all_destinations,
                    all_sources: all_sources
                }} AS tables
            RETURN tables
        """,
        {
            "edge": edge_id,
        },
        timeout=10000,
    )

    tables = []

    for node in result.result_set:
        table = node[0]

        columns = [
            GraphColumn(
                id=column.get("id"),
                name=column.get("name"),
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
                namespace=table.get("namespace"),
                data_source=table.get("data_source"),
                columns=columns,
                sources=[],
                destinations=table.get("destinations"),
                all_destinations=table.get("all_destinations"),
                all_sources=table.get("all_sources"),
            )
        )

    return tables

from typing import List, Literal, Optional, Tuple

from grai_client.endpoints.client import BaseClient
from grai_client.update import update
from grai_schemas.base import Edge, Node

from grai_source_snowflake.adapters import adapt_to_client
from grai_source_snowflake.loader import SnowflakeConnector


def get_nodes_and_edges(connector: SnowflakeConnector, version: Literal["v1"]) -> Tuple[List[Node], List[Edge]]:
    if version != "v1":
        raise NotImplementedError(f"No available implementation for client version {version}")

    with connector.connect() as conn:
        nodes, edges = conn.get_nodes_and_edges()

    nodes = adapt_to_client(nodes, version)
    edges = adapt_to_client(edges, version)
    return nodes, edges


def update_server(
    client: BaseClient,
    namespace: Optional[str] = None,
    account: Optional[str] = None,
    user: Optional[str] = None,
    password: Optional[str] = None,
    role: Optional[str] = None,
    warehouse: Optional[str] = None,
    database: Optional[str] = None,
    schema: Optional[str] = None,
) -> None:
    conn = SnowflakeConnector(
        account=account,
        user=user,
        password=password,
        role=role,
        warehouse=warehouse,
        database=database,
        schema=schema,
        namespace=namespace,
    )
    nodes, edges = get_nodes_and_edges(conn, client.id)

    update(client, nodes)
    update(client, edges)

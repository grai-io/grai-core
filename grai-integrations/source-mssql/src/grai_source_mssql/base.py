from typing import List, Literal, Optional, Tuple

from grai_client.endpoints.client import BaseClient
from grai_client.update import update
from grai_schemas.base import Edge, Node

from grai_source_mssql.adapters import adapt_to_client
from grai_source_mssql.loader import MsSQLConnector


def get_nodes_and_edges(connector: MsSQLConnector, version: Literal["v1"]) -> Tuple[List[Node], List[Edge]]:
    with connector.connect() as conn:
        nodes, edges = conn.get_nodes_and_edges()

    nodes = adapt_to_client(nodes, version)
    edges = adapt_to_client(edges, version)
    return nodes, edges


def update_server(
    client: BaseClient,
    database: Optional[str] = None,
    namespace: Optional[str] = None,
    user: Optional[str] = None,
    password: Optional[str] = None,
    protocol: Optional[str] = None,
    host: Optional[str] = None,
    port: Optional[str] = None,
    additional_connection_strings: Optional[List[str]] = None,
):
    conn = MsSQLConnector(
        database=database,
        user=user,
        password=password,
        protocol=protocol,
        host=host,
        port=port,
        additional_connection_strings=additional_connection_strings,
    )
    nodes, edges = get_nodes_and_edges(conn, client.id)
    update(client, nodes)
    update(client, edges)

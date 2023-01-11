from typing import List, Literal, Optional, Tuple

from grai_client.endpoints.client import BaseClient
from grai_client.schemas.edge import Edge
from grai_client.schemas.node import Node
from grai_client.update import update

from grai_source_postgres.adapters import adapt_to_client
from grai_source_postgres.loader import PostgresConnector


def get_nodes_and_edges(
    connector: PostgresConnector, version: Literal["v1"]
) -> Tuple[List[Node], List[Edge]]:
    with connector.connect() as conn:
        nodes, edges = conn.get_nodes_and_edges()

    nodes = adapt_to_client(nodes, version)
    edges = adapt_to_client(edges, version)
    return nodes, edges


def update_server(
    client: BaseClient,
    dbname: Optional[str] = None,
    namespace: Optional[str] = None,
    user: Optional[str] = None,
    password: Optional[str] = None,
    host: Optional[str] = None,
    port: Optional[str] = None,
):

    conn = PostgresConnector(
        dbname=dbname, user=user, password=password, host=host, port=port
    )
    nodes, edges = get_nodes_and_edges(conn, client.id)
    update(client, nodes)
    update(client, edges)

from typing import List, Literal, Optional, Tuple

from grai_client.endpoints.client import BaseClient
from grai_client.update import update
from grai_schemas.base import Edge, Node

from grai_source_redshift.adapters import adapt_to_client
from grai_source_redshift.loader import RedshiftConnector
from grai_source_redshift.package_definitions import config


def get_nodes_and_edges(connector: RedshiftConnector, version: Literal["v1"]) -> Tuple[List[Node], List[Edge]]:
    """

    Args:
        connector (RedshiftConnector):
        version (Literal["v1"]):

    Returns:

    Raises:

    """
    with connector as conn:
        nodes, edges = conn.get_nodes_and_edges()

    nodes = adapt_to_client(nodes, version)
    edges = adapt_to_client(edges, version)
    return nodes, edges


def update_server(
    client: BaseClient,
    namespace: str,
    database: Optional[str] = None,
    user: Optional[str] = None,
    password: Optional[str] = None,
    host: Optional[str] = None,
    port: Optional[str] = None,
):
    """

    Args:
        client (BaseClient):
        namespace (str):
        database (Optional[str], optional):  (Default value = None)
        user (Optional[str], optional):  (Default value = None)
        password (Optional[str], optional):  (Default value = None)
        host (Optional[str], optional):  (Default value = None)
        port (Optional[str], optional):  (Default value = None)

    Returns:

    Raises:

    """
    conn = RedshiftConnector(
        database=database,
        user=user,
        password=password,
        host=host,
        port=port,
        namespace=namespace,
    )
    nodes, edges = get_nodes_and_edges(conn, client.id)

    update(client, nodes)
    update(client, edges)

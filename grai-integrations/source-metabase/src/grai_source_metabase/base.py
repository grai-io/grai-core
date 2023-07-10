from typing import List, Literal, Optional, Tuple

from grai_client.endpoints.client import BaseClient
from grai_client.update import update
from grai_schemas.base import Edge, Node

from grai_source_metabase.adapters import adapt_to_client
from grai_source_metabase.loader import MetabaseConnector


def get_nodes_and_edges(connector: MetabaseConnector, version: Literal["v1"]) -> Tuple[List[Node], List[Edge]]:
    """

    Args:
        connector (MetabaseConnector):
        version (Literal["v1"]):

    Returns:

    Raises:

    """
    nodes = connector.get_nodes()
    edges = connector.get_edges()

    nodes = adapt_to_client(nodes, version)
    edges = adapt_to_client(edges, version)
    return nodes, edges


def update_server(
    client: BaseClient,
    namespaces: Optional = None,
    metabase_namespace: Optional[str] = None,
    username: Optional[str] = None,
    password: Optional[str] = None,
    endpoint: Optional[str] = None,
):
    """

    Args:
        password:
        username: Optional[str]
        client:
        namespaces:  (Default value = None)
        metabase_namespace:  (Default value = None)
        endpoint:  (Default value = None)

    Returns:

    Raises:

    """
    kwargs = {
        "namespaces": namespaces,
        "metabase_namespace": metabase_namespace,
        "username": username,
        "password": password,
        "endpoint": endpoint,
    }
    kwargs = {k: v for k, v in kwargs.items() if v is not None}

    conn = MetabaseConnector(**kwargs)
    nodes, edges = get_nodes_and_edges(conn, "v1")

    update(client, nodes)
    update(client, edges)

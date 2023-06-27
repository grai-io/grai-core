from typing import List, Literal, Optional

from grai_client.endpoints.client import BaseClient
from grai_client.update import update
from grai_schemas.base import Node

from loader import MetabaseConnector
from adapters import adapt_to_client


def get_nodes(connector: MetabaseConnector, version: Literal["v1"]) -> List[Node]:
    """

    Args:
        connector (MetabaseConnector):
        version (Literal["v1"]):

    Returns:

    Raises:

    """
    nodes = connector.get_nodes()

    nodes = adapt_to_client(nodes, version)
    return nodes


def update_server(
    client: BaseClient,
    namespaces: Optional = None,
    default_namespace: Optional[str] = None,
    username: Optional[str] = None,
    password: Optional[str] = None,
    endpoint: Optional[str] = None,
):
    """

    Args:
        password: Optional[str]
        username: Optional[str]
        client (BaseClient):
        namespaces (Optional[NamespaceTypes], optional):  (Default value = None)
        default_namespace (Optional[str], optional):  (Default value = None)
        endpoint (Optional[str], optional):  (Default value = None)

    Returns:

    Raises:

    """
    kwargs = {
        "namespaces": namespaces,
        "default_namespace": default_namespace,
        "username": username,
        "password": password,
        "endpoint": endpoint,
    }
    kwargs = {k: v for k, v in kwargs.items() if v is not None}

    conn = MetabaseConnector(**kwargs)
    nodes = get_nodes(conn, client.id)

    update(client, nodes)

# git commit message - "chore:
from functools import partial
from typing import List, Literal, Optional, Tuple

from grai_client.endpoints.client import BaseClient
from grai_client.update import update
from grai_schemas.base import Edge, Node

from grai_source_fivetran.adapters import adapt_to_client
from grai_source_fivetran.loader import FivetranConnector, NamespaceTypes


def get_nodes_and_edges(connector: FivetranConnector, version: Literal["v1"]) -> Tuple[List[Node], List[Edge]]:
    nodes, edges = connector.get_nodes_and_edges()

    nodes = adapt_to_client(nodes, version)
    edges = adapt_to_client(edges, version)
    return nodes, edges


def update_server(
    client: BaseClient,
    namespaces: Optional[NamespaceTypes] = None,
    default_namespace: Optional[str] = None,
    api_key: Optional[str] = None,
    api_secret: Optional[str] = None,
    endpoint: Optional[str] = None,
    limit: Optional[int] = None,
    parallelization: Optional[int] = None,
):
    kwargs = {
        "namespaces": namespaces,
        "default_namespace": default_namespace,
        "api_key": api_key,
        "api_secret": api_secret,
        "endpoint": endpoint,
        "limit": limit,
        "parallelization": parallelization,
    }
    kwargs = {k: v for k, v in kwargs.items() if v is not None}

    conn = FivetranConnector(**kwargs)
    nodes, edges = get_nodes_and_edges(conn, client.id)
    update(client, nodes)
    update(client, edges)

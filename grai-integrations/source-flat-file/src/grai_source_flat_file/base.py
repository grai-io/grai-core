from typing import List, Literal, Optional, Tuple

from grai_client.endpoints.client import BaseClient
from grai_client.update import update

from grai_source_flat_file.adapters import adapt_to_client
from grai_source_flat_file.loader import build_nodes_and_edges


def get_nodes_and_edges(file_name: str, namespace: str, version: str = "v1"):
    if version != "v1":
        raise NotImplementedError(f"No implementation for version {version}")

    nodes, edges = build_nodes_and_edges(file_name, namespace)
    nodes = adapt_to_client(nodes)
    edges = adapt_to_client(edges)
    return nodes, edges


def update_server(
    client: BaseClient,
    file_name: str,
    namespace: Optional[str] = None,
):
    nodes, edges = get_nodes_and_edges(file_name, namespace, client.id)

    update(client, nodes)
    update(client, edges)

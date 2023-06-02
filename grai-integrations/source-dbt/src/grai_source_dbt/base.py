from typing import List, Literal, Tuple

from grai_client.endpoints.client import BaseClient
from grai_client.update import update
from grai_schemas.base import Edge, Node

from grai_source_dbt.processor import ManifestProcessor


def get_nodes_and_edges(manifest_file: str, namespace="default", version: str = "v1") -> Tuple[List[Node], List[Edge]]:
    """

    Args:
        manifest_file (str):
        namespace:  (Default value = "default")
        version (str, optional):  (Default value = "v1")

    Returns:

    Raises:

    """
    manifest = ManifestProcessor.load(manifest_file, namespace)
    return manifest.adapted_nodes, manifest.adapted_edges


def update_server(client: BaseClient, manifest_file: str, namespace: str = "default") -> Tuple[List[Node], List[Edge]]:
    """

    Args:
        client (BaseClient):
        manifest_file (str):
        namespace (str, optional):  (Default value = "default")

    Returns:

    Raises:

    """
    nodes, edges = get_nodes_and_edges(manifest_file, namespace, client.id)

    update(client, nodes)
    update(client, edges)

    return nodes, edges

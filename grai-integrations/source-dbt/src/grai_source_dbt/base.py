from typing import List, Literal, Tuple

from grai_client.endpoints.client import BaseClient
from grai_client.update import update
from grai_schemas.base import Edge, Node

from grai_source_dbt.adapters import adapt_to_client
from grai_source_dbt.processor import ManifestProcessor


def get_nodes_and_edges(manifest_file: str, namespace="default", version: str = "v1") -> Tuple[List[Node], List[Edge]]:
    manifest = ManifestProcessor.load(manifest_file, namespace)
    return manifest.adapted_nodes, manifest.adapted_edges


def update_server(client: BaseClient, manifest_file: str, namespace: str = "default") -> Tuple[List[Node], List[Edge]]:
    nodes, edges = get_nodes_and_edges(manifest_file, namespace, client.id)

    update(client, nodes)
    update(client, edges)

    return nodes, edges

from typing import List, Literal, Tuple

from grai_client.endpoints.client import BaseClient
from grai_client.endpoints.v1.client import ClientV1
from grai_client.schemas.edge import Edge
from grai_client.schemas.node import Node
from grai_client.update import update
from grai_source_dbt.adapters import adapt_to_client
from grai_source_dbt.base import update_server
from grai_source_dbt.loader import DBTGraph, Manifest
from grai_source_dbt.test_utils import get_manifest_file


def get_nodes_and_edges(
    manifest_file: str, version: Literal["v1"]
) -> Tuple[List[Node], List[Edge]]:
    manifest = Manifest.load(manifest_file)
    dbt_graph = DBTGraph(manifest)

    nodes = adapt_to_client(dbt_graph.nodes, version)
    edges = adapt_to_client(dbt_graph.edges, version)
    return nodes, edges


def update_server(client: BaseClient, manifest_file: str):
    nodes, edges = get_nodes_and_edges(manifest_file, client.id)


client = ClientV1("localhost", "8000")
client.set_authentication_headers("null@grai.io", "super_secret")


update_server(client, get_manifest_file())

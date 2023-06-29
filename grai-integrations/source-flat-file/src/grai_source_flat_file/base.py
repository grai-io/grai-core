from typing import List, Tuple

from grai_client.endpoints.client import BaseClient
from grai_client.integrations.base import (
    CombinedNodesAndEdgesMixin,
    GraiIntegrationImplementationV1,
)
from grai_schemas.base import SourcedEdge, SourcedNode

from grai_source_flat_file.adapters import adapt_to_client
from grai_source_flat_file.loader import build_nodes_and_edges


class DbtIntegration(GraiIntegrationImplementationV1, CombinedNodesAndEdgesMixin):
    def __init__(self, client: BaseClient, source_name: str, file_name: str, namespace: str):
        super().__init__(client, source_name)

        self.file_name = file_name
        self.namespace = namespace

    def get_nodes_and_edges(self) -> Tuple[List[SourcedNode], List[SourcedEdge]]:
        nodes, edges = build_nodes_and_edges(self.file_name, self.namespace)
        nodes = adapt_to_client(nodes)
        edges = adapt_to_client(edges)
        return nodes, edges

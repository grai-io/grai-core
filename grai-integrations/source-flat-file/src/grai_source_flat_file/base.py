from typing import List, Optional, Tuple

from grai_client.endpoints.client import BaseClient
from grai_client.integrations.base import (
    CombinedNodesAndEdgesMixin,
    GraiIntegrationImplementationV1,
)
from grai_schemas.base import SourcedEdge, SourcedNode
from grai_schemas.v1.source import SourceSpec

from grai_source_flat_file.adapters import adapt_to_client
from grai_source_flat_file.loader import build_nodes_and_edges


class FlatFileIntegration(CombinedNodesAndEdgesMixin, GraiIntegrationImplementationV1):
    def __init__(
        self,
        file_name: str,
        namespace: str,
        client: Optional[BaseClient] = None,
        source_name: Optional[str] = None,
        source: Optional[SourceSpec] = None,
    ):
        super().__init__(client, source_name, source)

        self.file_name = file_name
        self.namespace = namespace

    def get_nodes_and_edges(self) -> Tuple[List[SourcedNode], List[SourcedEdge]]:
        nodes, edges = build_nodes_and_edges(self.file_name, self.namespace)
        nodes = adapt_to_client(nodes, self.source, self.version)
        edges = adapt_to_client(edges, self.source, self.version)
        return nodes, edges

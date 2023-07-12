import os
from typing import List, Optional, Tuple

from grai_client.integrations.base import (
    CombinedNodesAndEdgesMixin,
    GraiIntegrationImplementation,
)
from grai_schemas.base import SourcedEdge, SourcedNode
from grai_schemas.v1.source import SourceV1

from grai_source_flat_file.adapters import adapt_to_client
from grai_source_flat_file.loader import LOADER_MAP, build_nodes_and_edges


class FlatFileIntegration(CombinedNodesAndEdgesMixin, GraiIntegrationImplementation):
    def __init__(
        self,
        file_name: str,
        namespace: str,
        source: SourceV1,
        version: Optional[str] = None,
    ):
        super().__init__(source, version)

        self.file_name = file_name
        self.namespace = namespace

    def get_nodes_and_edges(self) -> Tuple[List[SourcedNode], List[SourcedEdge]]:
        nodes, edges = build_nodes_and_edges(self.file_name, self.namespace)
        nodes = adapt_to_client(nodes, self.source, self.version)
        edges = adapt_to_client(edges, self.source, self.version)
        return nodes, edges

    def ready(self) -> bool:
        file_ext = os.path.splitext(self.file_name)[-1]
        return file_ext in LOADER_MAP

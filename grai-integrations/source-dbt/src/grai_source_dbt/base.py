from typing import List, Optional, Tuple

from grai_client.endpoints.client import BaseClient
from grai_client.integrations.base import (
    CombinedNodesAndEdgesMixin,
    GraiIntegrationImplementationV1,
)
from grai_schemas.base import SourcedEdge, SourcedNode
from grai_schemas.v1.source import SourceSpec

from grai_source_dbt.processor import ManifestProcessor


class DbtIntegration(CombinedNodesAndEdgesMixin, GraiIntegrationImplementationV1):
    def __init__(
        self,
        manifest_file: str,
        client: Optional[BaseClient] = None,
        source_name: Optional[str] = None,
        source: Optional[SourceSpec] = None,
        namespace: Optional[str] = "default",
    ):
        super().__init__(client, source_name, source)

        self.manifest_file = manifest_file
        self.namespace = namespace

    def get_nodes_and_edges(self) -> Tuple[List[SourcedNode], List[SourcedEdge]]:
        manifest = ManifestProcessor.load(self.manifest_file, self.namespace, self.source)
        return manifest.adapted_nodes, manifest.adapted_edges

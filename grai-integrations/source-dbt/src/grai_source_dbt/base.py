from typing import List, Optional, Tuple

from grai_client.endpoints.client import BaseClient
from grai_client.integrations.base import (
    CombinedNodesAndEdgesMixin,
    GraiIntegrationImplementationV1,
)
from grai_schemas.base import SourcedEdge, SourcedNode

from grai_source_dbt.processor import ManifestProcessor


class DbtIntegration(GraiIntegrationImplementationV1, CombinedNodesAndEdgesMixin):
    def __init__(
        self,
        client: BaseClient,
        source_name: str,
        manifest_file: str,
        namespace: Optional[str] = "default",
    ):
        super().__init__(client, source_name)

        self.manifest_file = manifest_file
        self.namespace = namespace

    def get_nodes_and_edges(self) -> Tuple[List[SourcedNode], List[SourcedEdge]]:
        manifest = ManifestProcessor.load(self.manifest_file, self.namespace, self.source)
        return manifest.adapted_nodes, manifest.adapted_edges

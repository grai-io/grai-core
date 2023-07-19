from typing import List, Optional, Tuple

from grai_client.integrations.base import (
    CombinedNodesAndEdgesMixin,
    GraiIntegrationImplementation,
)
from grai_schemas.base import SourcedEdge, SourcedNode
from grai_schemas.v1.source import SourceV1

from grai_source_dbt.processor import ManifestProcessor


class DbtIntegration(CombinedNodesAndEdgesMixin, GraiIntegrationImplementation):
    def __init__(
        self,
        manifest_file: str,
        source: SourceV1,
        version: Optional[str] = None,
        namespace: Optional[str] = "default",
    ):
        super().__init__(source, version)

        self.manifest_file = manifest_file
        self.namespace = namespace

    def get_nodes_and_edges(self) -> Tuple[List[SourcedNode], List[SourcedEdge]]:
        manifest = ManifestProcessor.load(self.manifest_file, self.namespace, self.source)
        return manifest.adapted_nodes, manifest.adapted_edges

    def ready(self) -> bool:
        _ = ManifestProcessor.load(self.manifest_file, self.namespace, self.source)
        return True

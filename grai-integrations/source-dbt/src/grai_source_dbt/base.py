from functools import cached_property
from typing import List, Optional, Tuple, Union

from grai_schemas.base import SourcedEdge, SourcedNode
from grai_schemas.integrations.base import GraiIntegrationImplementation
from grai_schemas.v1.source import SourceV1

from grai_source_dbt.processor import ManifestProcessor


class DbtIntegration(GraiIntegrationImplementation):
    def __init__(
        self,
        manifest_data: Union[str, dict],
        source: SourceV1,
        version: Optional[str] = None,
        namespace: Optional[str] = "default",
    ):
        super().__init__(source, version)

        self.manifest_data = manifest_data
        self.namespace = namespace

    @cached_property
    def manifest(self) -> ManifestProcessor:
        return ManifestProcessor.load(self.manifest_data, self.namespace, self.source)

    def nodes(self) -> List[SourcedNode]:
        return self.manifest.adapted_nodes

    def edges(self) -> List[SourcedEdge]:
        return self.manifest.adapted_edges

    def get_nodes_and_edges(self) -> Tuple[List[SourcedNode], List[SourcedEdge]]:
        return self.nodes(), self.edges()

    def ready(self) -> bool:
        manifest = self.manifest
        return True

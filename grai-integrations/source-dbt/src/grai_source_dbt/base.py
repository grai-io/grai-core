from functools import cached_property
from typing import List, Optional, Tuple, Union

from grai_schemas.base import SourcedEdge, SourcedNode
from grai_schemas.integrations.base import GraiIntegrationImplementation
from grai_schemas.v1.source import SourceV1

from grai_source_dbt.processor import ManifestProcessor


class DbtIntegration(GraiIntegrationImplementation):
    """A class for extracting Grai compliant metadata from a dbt manifest.json file.

    Attributes:
        manifest_data: A dictionary parsing of a manifest.json file
        namespace: The Grai namespace to associate with output from the integration

    """

    def __init__(
        self,
        manifest_data: Union[str, dict],
        source: SourceV1,
        version: Optional[str] = None,
        namespace: Optional[str] = "default",
    ):
        """Initializes the dbt integration.

        Args:
            manifest_data: Either a string path to a manifest.json file, or a dictionary parsing of a manifest.json file
            source: The Grai data source to associate with output from the integration. More information about source objects is available in the `grai_schemas` library.
            version: The Grai data version to associate with output from the integration
            namespace: The Grai namespace to associate with output from the integration

        """
        super().__init__(source, version)

        self.manifest_data = manifest_data
        self.namespace = namespace

    @cached_property
    def manifest(self) -> ManifestProcessor:
        """Returns a ManifestProcessor object for the manifest.json file"""
        return ManifestProcessor.load(self.manifest_data, self.namespace, self.source)

    def nodes(self) -> List[SourcedNode]:
        """Returns a list of SourcedNode objects"""
        return self.manifest.adapted_nodes

    def edges(self) -> List[SourcedEdge]:
        """Returns a list of SourcedEdge objects"""
        return self.manifest.adapted_edges

    def get_nodes_and_edges(self) -> Tuple[List[SourcedNode], List[SourcedEdge]]:
        """Returns a tuple of lists of SourcedNode and SourcedEdge objects"""
        return self.nodes(), self.edges()

    def ready(self) -> bool:
        """Returns True if the integration is ready to run"""
        manifest = self.manifest
        return True

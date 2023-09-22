import os
from functools import cache
from typing import List, Optional, Tuple

from grai_schemas.base import SourcedEdge, SourcedNode
from grai_schemas.integrations.base import GraiIntegrationImplementation
from grai_schemas.v1.source import SourceV1

from grai_source_flat_file.adapters import adapt_to_client
from grai_source_flat_file.loader import LOADER_MAP, build_nodes_and_edges


class FlatFileIntegration(GraiIntegrationImplementation):
    """A class for extracting Grai compliant metadata from flat files like csv and parquet.

    Attributes:
        file_name: A path to the file
        namespace: The Grai namespace to associate with output from the integration

    """

    def __init__(
        self,
        file_name: str,
        namespace: str,
        source: SourceV1,
        version: Optional[str] = None,
    ):
        """Initializes the Flat File integration.

        Args:
            file_name: A path to the file
            namespace: The Grai namespace to associate with output from the integration
            source: The Grai data source to associate with output from the integration. More information about source objects is available in the `grai_schemas` library.
            version: The Grai data version to associate with output from the integration
        """
        super().__init__(source, version)

        self.file_name = file_name
        self.namespace = namespace

    @cache
    def get_nodes_and_edges(self) -> Tuple[List[SourcedNode], List[SourcedEdge]]:
        """Returns a tuple of lists of SourcedNode and SourcedEdge objects"""
        nodes, edges = build_nodes_and_edges(self.file_name, self.namespace)
        nodes = adapt_to_client(nodes, self.source, self.version)
        edges = adapt_to_client(edges, self.source, self.version)
        return nodes, edges

    def nodes(self) -> List[SourcedNode]:
        """Returns a list of SourcedNode objects"""
        return self.get_nodes_and_edges()[0]

    def edges(self) -> List[SourcedEdge]:
        """Returns a list of SourcedEdge objects"""
        return self.get_nodes_and_edges()[1]

    def ready(self) -> bool:
        """Returns True if the integration is ready to run"""
        file_ext = os.path.splitext(self.file_name)[-1]
        return file_ext in LOADER_MAP

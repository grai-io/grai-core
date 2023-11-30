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
        file_ref: str,
        namespace: str,
        source: SourceV1,
        file_ext: Optional[str] = None,
        table_name: Optional[str] = None,
        file_location: Optional[str] = None,
        version: Optional[str] = None,
    ):
        """Initializes the Flat File integration.

        Args:
            file_ref: A loadable file reference
            namespace: The Grai namespace to associate with output from the integration
            source: The Grai data source to associate with output from the integration. More information about source objects is available in the `grai_schemas` library.
            version: The Grai data version to associate with output from the integration
        """
        super().__init__(source, version)
        try:
            default_table_name, default_file_ext = os.path.splitext(file_ref)
        except:
            default_table_name, default_file_ext = None, None

        self.file_ref = file_ref
        if file_ext is not None:
            self.file_ext = file_ext
        elif default_file_ext is not None:
            self.file_ext = default_file_ext
        else:
            message = (
                f"Could not extract the file type from the provided file object of type `{type(self.file_ref)}`. "
                "You must either provide the file_ref as a string or provide an explicit `file_ext` value."
            )
            raise ValueError(message)

        if table_name is not None:
            self.table_name = table_name
        elif default_table_name is not None:
            self.table_name = default_table_name
        else:
            message = (
                f"Could not extract a table name from the provided file object of type `{type(self.file_ref)}`. "
                "You must either provide the file_ref as a string or provide an explicit `table_name` value."
            )
            raise ValueError(message)

        self.file_location = file_location
        if self.file_location is None and isinstance(self.file_ref, str):
            self.file_location = self.file_ref

        self.namespace = namespace

    @cache
    def get_nodes_and_edges(self) -> Tuple[List[SourcedNode], List[SourcedEdge]]:
        """Returns a tuple of lists of SourcedNode and SourcedEdge objects"""
        nodes, edges = build_nodes_and_edges(
            self.file_ref, self.file_ext, self.table_name, self.file_location, self.namespace
        )
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
        return self.file_ext in LOADER_MAP

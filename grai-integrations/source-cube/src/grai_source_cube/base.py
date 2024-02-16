from functools import cached_property
from typing import List, Optional, Tuple, Union
from warnings import warn

from grai_schemas.base import SourcedEdge, SourcedNode
from grai_schemas.integrations.base import GraiIntegrationImplementation
from grai_schemas.v1.source import SourceV1
from requests import HTTPError

from grai_source_cube.loader import CubeConnector


class CubeIntegration(GraiIntegrationImplementation):
    """A class for extracting Grai compliant metadata from the Cube.dev REST API

    Attributes:
        namespace: The Grai namespace to associate with output from the integration

    """

    def __init__(
        self,
        source: SourceV1,
        namespace: str,
        version: Optional[str] = None,
    ):
        """Initializes the dbt integration.

        Args:
            source: The Grai data source to associate with output from the integration. More information about source objects is available in the `grai_schemas` library.
            version: The Grai data version to associate with output from the integration
            namespace: The Grai namespace to associate with output from the integration

        """
        super().__init__(source, version)

        self.namespace = namespace
        self.connector = CubeConnector(namespace=namespace)

    def nodes(self) -> List[SourcedNode]:
        """Returns a list of SourcedNode objects"""
        # adapted nodes
        pass

    def edges(self) -> List[SourcedEdge]:
        """Returns a list of SourcedEdge objects"""
        # adapted edges
        pass

    def get_nodes_and_edges(self) -> Tuple[List[SourcedNode], List[SourcedEdge]]:
        """Returns a tuple of lists of SourcedNode and SourcedEdge objects"""
        return self.nodes(), self.edges()

    def ready(self) -> bool:
        """Returns True if the integration is ready to run"""
        response = self.ready()
        try:
            response.raise_for_status()
            return True
        except HTTPError:
            return False
        except Exception as e:
            warn("An unexpected error occurred while checking the readiness of the cube API.")
            return False

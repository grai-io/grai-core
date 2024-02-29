from typing import Dict, List, Optional, Tuple, Union
from warnings import warn

from grai_schemas.base import SourcedEdge, SourcedNode
from grai_schemas.integrations.base import GraiIntegrationImplementation
from grai_schemas.v1.source import SourceV1
from grai_source_cube.adapters import adapt_to_client
from grai_source_cube.connector import CubeConnector, CubeSourceMap
from grai_source_cube.settings import CubeApiConfig
from requests import HTTPError


def process_namespace_map(namespace_map: Optional[Union[CubeSourceMap, Dict]]) -> CubeSourceMap:
    if namespace_map is None:
        result = CubeSourceMap()
    elif isinstance(namespace_map, dict):
        try:
            result = CubeSourceMap(map=namespace_map)
        except Exception as e:
            raise ValueError(f"Could not parse the `namespace_map` from the provided dictionary: {e}")
    elif not isinstance(namespace_map, CubeSourceMap):
        raise ValueError("The `namespace_map` must be a `CubeSourceMap` or a dictionary")

    return result


class CubeIntegration(GraiIntegrationImplementation):
    """A class for extracting Grai compliant metadata from the Cube.dev REST API

    Attributes:
        namespace: The Grai namespace to associate with output from the integration

    """

    def __init__(
        self,
        source: SourceV1,
        namespace: str,
        config: CubeApiConfig,
        namespace_map: Optional[Union[CubeSourceMap, Dict]] = None,
        version: Optional[str] = None,
    ):
        """Initializes the dbt integration.

        Args:
            source: The Grai data source to associate with output from the integration.
            version: The Grai data version to associate with output from the integration
            namespace: The Grai namespace to associate with output from the integration

        """
        namespace_map = process_namespace_map(namespace_map)
        super().__init__(source, version)

        self.namespace = namespace
        self.connector = CubeConnector(namespace_map=namespace_map.map, config=config)

    def nodes(self) -> List[SourcedNode]:
        """Returns a list of SourcedNode objects"""
        # adapted nodes
        return adapt_to_client(self.connector.nodes, self.source, self.version)

    def edges(self) -> List[SourcedEdge]:
        """Returns a list of SourcedEdge objects"""
        # adapted edges
        return adapt_to_client(self.connector.edges, self.source, self.version)

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
        except Exception:
            warn("An unexpected error occurred while checking the readiness of the cube API.")
            return False

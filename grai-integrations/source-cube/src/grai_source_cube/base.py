import json
from typing import Dict, List, Optional, Tuple, Union
from warnings import warn

from grai_schemas.base import SourcedEdge, SourcedNode
from grai_schemas.integrations.base import GraiIntegrationImplementation
from grai_schemas.v1.source import SourceSpec, SourceV1
from grai_source_cube.adapters import adapt_to_client
from grai_source_cube.connector import CubeConnector, NamespaceMap
from grai_source_cube.settings import CubeApiConfig
from requests import HTTPError


def process_namespace_map(namespace_map: Optional[Union[NamespaceMap, Dict, str]]) -> NamespaceMap:
    if namespace_map is None:
        result = NamespaceMap()
    elif isinstance(namespace_map, dict):
        try:
            result = NamespaceMap(map=namespace_map)
        except Exception as e:
            raise ValueError(f"Could not parse the `namespace_map` from the provided dictionary: {e}")
    elif isinstance(namespace_map, str):
        try:
            result = NamespaceMap(map=json.loads(namespace_map))
        except Exception as e:
            raise ValueError(f"Could not parse the `namespace_map` from the provided string: {e}")
    elif not isinstance(namespace_map, NamespaceMap):
        raise ValueError("The `namespace_map` must be a `CubeSourceMap`, dictionary, or json string.")
    else:
        raise ValueError("The `namespace_map` must be a `CubeSourceMap`, dictionary, or json string.")
    return result


class CubeIntegration(GraiIntegrationImplementation):
    """A class for extracting Grai compliant metadata from the Cube.dev REST API"""

    def __init__(
        self,
        source: Union[SourceV1, SourceSpec],
        namespace: str,
        config: Optional[CubeApiConfig] = None,
        namespace_map: Optional[Union[NamespaceMap, Dict, str]] = None,
        version: str = "v1",
    ):
        """Initializes the Cube.js integration.

        Args:
            source: The Grai data source to associate with output from the integration.
            namespace: The Grai namespace to associate with output from the integration
            config: The connection configuration for your cube API. If not provided, an effort will be made to load
                these from the environment.
            namespace_map: An optional mapping between cube data sources and Grai namespaces
            version: The version of the Grai API to use for the integration
        """
        namespace_map = process_namespace_map(namespace_map)
        source: SourceV1 = source if isinstance(source, SourceV1) else SourceV1.from_spec(source)
        super().__init__(source, version)

        self.connector = CubeConnector(namespace=namespace, namespace_map=namespace_map.map, config=config)

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
        response = self.connector.ready()
        try:
            response.raise_for_status()
            return True
        except HTTPError:
            return False
        except Exception:
            warn("An unexpected error occurred while checking the readiness of the cube API.")
            return False

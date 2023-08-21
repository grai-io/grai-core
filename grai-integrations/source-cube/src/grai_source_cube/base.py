from typing import Dict, List, Optional, Union

from grai_client.integrations.base import (
    GraiIntegrationImplementation,
    SeparateNodesAndEdgesMixin,
)
from grai_schemas.base import SourcedEdge, SourcedNode
from grai_schemas.v1.source import SourceV1

from grai_source_cube.adapters import adapt_to_client
from grai_source_cube.loader import CubeConnector


class CubeIntegration(SeparateNodesAndEdgesMixin, GraiIntegrationImplementation):
    def __init__(
        self,
        source: SourceV1,
        version: Optional[str] = None,
        metabase_namespace: Optional[str] = None,
        namespace_map: Optional[Union[str, Dict[int, str]]] = None,
        endpoint: Optional[str] = None,
        username: Optional[str] = None,
        password: Optional[str] = None,
    ):
        super().__init__(source, version)

        self.connector = CubeConnector(
            metabase_namespace=metabase_namespace,
            namespace_map=namespace_map,
            username=username,
            password=password,
            endpoint=endpoint,
        )

    def ready(self) -> bool:
        # quick method to validate the connection was authenticated, has appropriate permissions, etc...
        self.connector.authenticate()
        return True

    def nodes(self) -> List[SourcedNode]:
        # converts the node output of the loader to data structured for Grai
        nodes = adapt_to_client(self.connector.get_nodes(), self.source, self.version)
        return nodes

    def edges(self) -> List[SourcedEdge]:
        # converts the edge output of the loader to data structured for Grai
        edges = adapt_to_client(self.connector.get_edges(), self.source, self.version)
        return edges

from typing import Dict, List, Optional, Union

from grai_client.integrations.base import (
    GraiIntegrationImplementation,
    SeparateNodesAndEdgesMixin,
)
from grai_schemas.base import SourcedEdge, SourcedNode
from grai_schemas.v1.source import SourceV1

from grai_source_metabase.adapters import adapt_to_client
from grai_source_metabase.loader import MetabaseConnector


class MetabaseIntegration(SeparateNodesAndEdgesMixin, GraiIntegrationImplementation):
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

        self.connector = MetabaseConnector(
            metabase_namespace=metabase_namespace,
            namespace_map=namespace_map,
            username=username,
            password=password,
            endpoint=endpoint,
        )

    def ready(self) -> bool:
        self.connector.authenticate()
        return True

    def nodes(self) -> List[SourcedNode]:
        nodes = adapt_to_client(self.connector.get_nodes(), self.source, self.version)
        return nodes

    def edges(self) -> List[SourcedEdge]:
        edges = adapt_to_client(self.connector.get_edges(), self.source, self.version)
        return edges

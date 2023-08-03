from typing import List, Optional, Tuple

from grai_client.integrations.base import (
    CombinedNodesAndEdgesMixin,
    GraiIntegrationImplementation,
)
from grai_schemas.base import SourcedEdge, SourcedNode
from grai_schemas.v1.source import SourceV1

from grai_source_looker.adapters import adapt_to_client
from grai_source_looker.loader import LookerAPI


class LookerIntegration(CombinedNodesAndEdgesMixin, GraiIntegrationImplementation):
    def __init__(
        self,
        source: SourceV1,
        version: Optional[str] = None,
        base_url: Optional[str] = None,
        client_id: Optional[str] = None,
        client_secret: Optional[str] = None,
        verify_ssl: Optional[bool] = None,
        namespace: Optional[str] = None,
    ):
        super().__init__(source, version)

        self.connector = LookerAPI(
            base_url=base_url,
            client_id=client_id,
            client_secret=client_secret,
            verify_ssl=verify_ssl,
            namespace=namespace,
        )

    def ready(self) -> bool:
        self.connector.get_user()
        return True

    def get_nodes_and_edges(self) -> Tuple[List[SourcedNode], List[SourcedEdge]]:
        nodes, edges = self.connector.get_nodes_and_edges()

        nodes = adapt_to_client(nodes, self.source, self.version)
        edges = adapt_to_client(edges, self.source, self.version)

        return nodes, edges

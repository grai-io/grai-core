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

    def validate_nodes_and_edges(self, nodes: List[SourcedNode], edges: List[SourcedEdge]):
        """

        Args:
            nodes (List[Node]):
            edges (List[Edge]):

        Returns:

        Raises:

        """
        node_hashes = {hash(node) for node in nodes}
        if (n_hashes := len(node_hashes)) != len(nodes):
            message = (
                f"The Fivetran connection generated {len(nodes) - n_hashes} duplicated nodes. "
                f"This is likely because there are multiple Fivetran tables with the same name. "
                f"You can disambiguate these tables by identifying them with different namespaces. Please "
                f"see the documentation for more information. https://docs.grai.io/integrations/fivetran"
            )
            raise ValueError(message)

    def get_nodes_and_edges(self) -> Tuple[List[SourcedNode], List[SourcedEdge]]:
        nodes, edges = self.connector.get_nodes_and_edges()

        print(nodes)
        print(edges)

        nodes = adapt_to_client(nodes, self.source, self.version)
        edges = adapt_to_client(edges, self.source, self.version)
        # self.validate_nodes_and_edges(nodes, edges)
        return nodes, edges

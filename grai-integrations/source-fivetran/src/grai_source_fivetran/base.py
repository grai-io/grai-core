from typing import List, Optional, Tuple

from grai_client.integrations.base import (
    CombinedNodesAndEdgesMixin,
    GraiIntegrationImplementation,
)
from grai_schemas.base import SourcedEdge, SourcedNode
from grai_schemas.v1.source import SourceV1

from grai_source_fivetran.adapters import adapt_to_client
from grai_source_fivetran.loader import FivetranConnector, NamespaceTypes


class FivetranIntegration(CombinedNodesAndEdgesMixin, GraiIntegrationImplementation):
    def __init__(
        self,
        source: SourceV1,
        version: Optional[str] = None,
        namespaces: Optional[NamespaceTypes] = None,
        default_namespace: Optional[str] = None,
        parallelization: int = 10,
        api_key: Optional[str] = None,
        api_secret: Optional[str] = None,
        endpoint: Optional[str] = None,
        limit: Optional[int] = None,
    ):
        super().__init__(source, version)

        self.connector = FivetranConnector(
            namespaces=namespaces,
            default_namespace=default_namespace,
            parallelization=parallelization,
            api_key=api_key,
            api_secret=api_secret,
            endpoint=endpoint,
            limit=limit,
        )

    def ready(self) -> bool:
        self.connector.has_query_permissions()
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

        nodes = adapt_to_client(nodes, self.source, self.version)
        edges = adapt_to_client(edges, self.source, self.version)
        self.validate_nodes_and_edges(nodes, edges)
        return nodes, edges

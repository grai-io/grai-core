from functools import cache
from typing import List, Optional, Tuple

from grai_schemas.base import SourcedEdge, SourcedNode
from grai_schemas.integrations.base import GraiIntegrationImplementation
from grai_schemas.v1.source import SourceV1

from grai_source_fivetran.adapters import adapt_to_client
from grai_source_fivetran.loader import FivetranConnector, NamespaceTypes


class FivetranIntegration(GraiIntegrationImplementation):
    """A class for extracting Grai compliant metadata from the Fivetran API.

    Attributes:
        connector: The connector responsible for communicating with the Fivetran api.

    """

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
        """Initializes the Fivetran integration.

        Args:
            source: The Grai data source to associate with output from the integration. More information about source objects is available in the `grai_schemas` library.
            version: The Grai data version to associate with output from the integration
            default_namespace: The default Grai namespace to associate with output from the integration
            namespaces: A dictionary of namespaces to use for the integration. The keys of the dictionary should be the namespace names, and the values should be a list of Fivetran connectors to use for that namespace. If no namespaces are provided, the integration will use the default namespace.
            parallelization: The number of parallel connections to make with the Fivetran API
            api_key: A Fivetran API key
            api_secret: A Fivetran API secret
            endpoint: Your Fivetran API endpoint. Usually https://api.fivetran.com/v1
            limit: The maximum number of results to return in each API call
        """
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
        """Returns True if the integration is ready to run"""
        self.connector.has_query_permissions()
        return True

    @cache
    def get_nodes_and_edges(self) -> Tuple[List[SourcedNode], List[SourcedEdge]]:
        """Returns a tuple of lists of SourcedNode and SourcedEdge objects"""
        nodes, edges = self.connector.get_nodes_and_edges()

        nodes = adapt_to_client(nodes, self.source, self.version)
        edges = adapt_to_client(edges, self.source, self.version)

        node_hashes = {hash(node) for node in nodes}
        if (n_hashes := len(node_hashes)) != len(nodes):
            message = (
                f"The Fivetran connection generated {len(nodes) - n_hashes} duplicated nodes. "
                f"This is likely because there are multiple Fivetran tables with the same name. "
                f"You can disambiguate these tables by identifying them with different namespaces. Please "
                f"see the documentation for more information. https://docs.grai.io/integrations/fivetran"
            )
            raise ValueError(message)
        return nodes, edges

    def nodes(self) -> List[SourcedNode]:
        """ Returns a list of SourcedNode objects""" ""
        return self.get_nodes_and_edges()[0]

    def edges(self) -> List[SourcedEdge]:
        """Returns a list of SourcedEdge objects"""
        return self.get_nodes_and_edges()[1]

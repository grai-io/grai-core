from functools import cache
from typing import Dict, List, Optional, Tuple

from grai_schemas.base import SourcedEdge, SourcedNode
from grai_schemas.integrations.base import GraiIntegrationImplementation
from grai_schemas.v1.source import SourceV1

from grai_source_looker.adapters import adapt_to_client
from grai_source_looker.loader import LookerAPI


class LookerIntegration(GraiIntegrationImplementation):
    """A class for extracting Grai compliant metadata from Looker.

    Attributes:
        connector: The Looker connector responsible for communicating with the Looker API.

    """

    def __init__(
        self,
        source: SourceV1,
        version: Optional[str] = None,
        base_url: Optional[str] = None,
        client_id: Optional[str] = None,
        client_secret: Optional[str] = None,
        verify_ssl: Optional[bool] = None,
        namespace: Optional[str] = None,
        namespaces: Optional[Dict[str, str]] = None,
    ):
        """Initializes the Looker Integration.

        Args:
            source: The Grai data source to associate with output from the integration. More information about source objects is available in the `grai_schemas` library.
            version: The Grai data version to associate with output from the integration
            base_url: The base url for the Looker API. This should exclude the /api path.
            client_id: The client id for the Looker API.
            client_secret: The client secret for the Looker API.
            verify_ssl: Whether or not to verify SSL certificates when connecting to the Looker API.
            namespace: The default Grai namespace to associate with output from the integration
            namespaces: A dictionary of namespaces to use for the integration. The keys of the dictionary should be the namespace names, and the values should be a list of Looker API endpoints to use for that namespace. If no namespaces are provided, the integration will use the default namespace.
        """
        super().__init__(source, version)

        self.connector = LookerAPI(
            base_url=base_url,
            client_id=client_id,
            client_secret=client_secret,
            verify_ssl=verify_ssl,
            namespace=namespace,
            namespaces=namespaces,
        )

    def ready(self) -> bool:
        """Returns True if the integration is ready to run"""
        self.connector.get_user()
        return True

    @cache
    def get_nodes_and_edges(self) -> Tuple[List[SourcedNode], List[SourcedEdge]]:
        """Returns a tuple of lists of SourcedNode and SourcedEdge objects"""
        nodes, edges = self.connector.get_nodes_and_edges()

        nodes = adapt_to_client(nodes, self.source, self.version)
        edges = adapt_to_client(edges, self.source, self.version)

        return nodes, edges

    def nodes(self) -> List[SourcedNode]:
        """Returns a list of SourcedNode objects"""
        return self.get_nodes_and_edges()[0]

    def edges(self) -> List[SourcedEdge]:
        """Returns a list of SourcedEdge objects"""
        return self.get_nodes_and_edges()[1]

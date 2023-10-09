from functools import cache
from typing import Dict, List, Optional, Tuple, Union

from grai_schemas.base import SourcedEdge, SourcedNode
from grai_schemas.integrations.base import GraiIntegrationImplementation
from grai_schemas.v1.source import SourceV1

from grai_source_metabase.adapters import adapt_to_client
from grai_source_metabase.loader import MetabaseConnector


class MetabaseIntegration(GraiIntegrationImplementation):
    """A class for extracting Grai compliant metadata from Metabase

    Attributes:
        connector: The Metabase connector responsible for communicating with the Metabase API.

    """

    def __init__(
        self,
        source: SourceV1,
        metabase_namespace: str,
        version: Optional[str] = None,
        namespace_map: Optional[Union[str, Dict[int, str]]] = None,
        endpoint: Optional[str] = None,
        username: Optional[str] = None,
        password: Optional[str] = None,
    ):
        """Initializes the Metabase integration.

        Args:
            source: The Grai data source to associate with output from the integration. More information about source objects is available in the `grai_schemas` library.
            version: The Grai data version to associate with output from the integration
            metabase_namespace: The Grai namespace to associate with Metabase specific lineage like questions and dashboards.
            namespace_map: A dictionary mapping Metabase database ids to Grai namespaces
            endpoint: The url of your Metabase instance
            username: The username to use when authenticating with Metabase
            password: The password to use when authenticating with Metabase
        """
        super().__init__(source, version)

        self.connector = MetabaseConnector(
            metabase_namespace=metabase_namespace,
            namespace_map=namespace_map,
            username=username,
            password=password,
            endpoint=endpoint,
        )

    def ready(self) -> bool:
        """Returns True if the integration is ready to run"""
        self.connector.authenticate()
        return True

    @cache
    def nodes(self) -> List[SourcedNode]:
        """Returns a list of SourcedNode objects"""
        nodes = adapt_to_client(self.connector.get_nodes(), self.source, self.version)
        return nodes

    @cache
    def edges(self) -> List[SourcedEdge]:
        """Returns a list of SourcedEdge objects"""
        edges = adapt_to_client(self.connector.get_edges(), self.source, self.version)
        return edges

    def get_nodes_and_edges(self) -> Tuple[List[SourcedNode], List[SourcedEdge]]:
        """Returns a tuple of lists of SourcedNode and SourcedEdge objects"""
        return self.nodes(), self.edges()

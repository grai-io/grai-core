from functools import cache
from typing import List, Optional, Tuple

from grai_client.integrations.base import EventMixin
from grai_schemas.base import Event, SourcedEdge, SourcedNode
from grai_schemas.integrations.base import GraiIntegrationImplementation
from grai_schemas.v1.source import SourceV1
from grai_source_dbt_cloud.loader import DbtCloudConnector


class DbtCloudIntegration(EventMixin, GraiIntegrationImplementation):
    """A class for extracting Grai compliant metadata from the dbt cloud API.

    Attributes:
        connector: The dbt cloud connector responsible for communicating with the dbt cloud api.

    """

    def __init__(
        self,
        api_key: str,
        source: SourceV1,
        version: Optional[str] = None,
        namespace: Optional[str] = "default",
    ):
        """Initializes the dbt cloud integration.

        Args:
            api_key: A dbt cloud api key
            source: The Grai data source to associate with output from the integration. More information about source objects is available in the `grai_schemas` library.
            version: The Grai data version to associate with output from the integration
            namespace: The Grai namespace to associate with output from the integration

        """
        super().__init__(source, version)

        self.connector = DbtCloudConnector(
            namespace=namespace,
            api_key=api_key,
            source=source,
        )

    @cache
    def get_nodes_and_edges(self) -> Tuple[List[SourcedNode], List[SourcedEdge]]:
        """Returns a tuple of lists of SourcedNode and SourcedEdge objects"""
        nodes, edges = self.connector.get_nodes_and_edges()
        return nodes, edges

    def nodes(self) -> List[SourcedNode]:
        """Returns a list of SourcedNode objects"""
        return self.get_nodes_and_edges()[0]

    def edges(self) -> List[SourcedEdge]:
        """Returns a list of SourcedEdge objects"""
        return self.get_nodes_and_edges()[1]

    def events(self, last_event_date: Optional[str]) -> List[Event]:
        """Returns a list of Event objects"""
        events = self.connector.get_events(last_event_date=last_event_date)
        return events

    def ready(self) -> bool:
        """Returns True if the integration is ready to run"""
        _ = self.connector.default_account
        return True

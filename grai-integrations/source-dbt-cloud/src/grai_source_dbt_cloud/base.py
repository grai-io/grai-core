from typing import List, Optional, Tuple

from grai_client.endpoints.client import BaseClient
from grai_client.integrations.base import (
    CombinedNodesAndEdgesMixin,
    EventMixin,
    GraiIntegrationImplementation,
)
from grai_schemas.base import SourcedEdge, SourcedNode
from grai_schemas.v1.source import SourceSpec
from grai_source_dbt_cloud.loader import DbtCloudConnector


class DbtCloudIntegration(EventMixin, CombinedNodesAndEdgesMixin, GraiIntegrationImplementation):
    def __init__(
        self,
        api_key: str,
        client: Optional[BaseClient] = None,
        source_name: Optional[str] = None,
        source: Optional[SourceSpec] = None,
        namespace: Optional[str] = "default",
    ):
        super().__init__(client, source_name, source)

        self.connector = DbtCloudConnector(
            namespace=namespace,
            api_key=api_key,
        )

    def get_nodes_and_edges(self) -> Tuple[List[SourcedNode], List[SourcedEdge]]:
        nodes, edges = self.connector.get_nodes_and_edges()
        return nodes, edges

    def events(self, last_event_date: Optional[str]):
        events = self.connector.get_events(last_event_date=last_event_date)
        return events

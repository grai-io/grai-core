from functools import cache
from typing import List, Optional, Tuple

from grai_client.integrations.base import EventMixin
from grai_schemas.base import Event, SourcedEdge, SourcedNode
from grai_schemas.integrations.base import GraiIntegrationImplementation
from grai_schemas.v1.source import SourceV1
from grai_source_dbt_cloud.loader import DbtCloudConnector


class DbtCloudIntegration(EventMixin, GraiIntegrationImplementation):
    def __init__(
        self,
        api_key: str,
        source: SourceV1,
        version: Optional[str] = None,
        namespace: Optional[str] = "default",
    ):
        super().__init__(source, version)

        self.connector = DbtCloudConnector(
            namespace=namespace,
            api_key=api_key,
            source=source,
        )

    @cache
    def get_nodes_and_edges(self) -> Tuple[List[SourcedNode], List[SourcedEdge]]:
        nodes, edges = self.connector.get_nodes_and_edges()
        return nodes, edges

    def nodes(self) -> List[SourcedNode]:
        return self.get_nodes_and_edges()[0]

    def edges(self) -> List[SourcedEdge]:
        return self.get_nodes_and_edges()[1]

    def events(self, last_event_date: Optional[str]) -> List[Event]:
        events = self.connector.get_events(last_event_date=last_event_date)
        return events

    def ready(self) -> bool:
        _ = self.connector.default_account
        return True

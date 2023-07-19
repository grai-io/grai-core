from typing import List, Optional, Union

from grai_client.integrations.base import (
    GraiIntegrationImplementation,
    SeparateNodesAndEdgesMixin,
)
from grai_schemas.v1.source import SourceV1

from grai_source_bigquery.adapters import adapt_to_client
from grai_source_bigquery.loader import BigqueryConnector, LoggingConnector


class BigQueryIntegration(SeparateNodesAndEdgesMixin, GraiIntegrationImplementation):
    def __init__(
        self,
        source: SourceV1,
        version: Optional[str] = None,
        namespace: Optional[str] = None,
        project: Optional[str] = None,
        dataset: Optional[Union[str, List[str]]] = None,
        credentials: Optional[str] = None,
        log_parsing: Optional[bool] = False,
        log_parsing_window: Optional[int] = 7,
    ):
        super().__init__(source, version)

        self.connector = (
            BigqueryConnector(
                project=project,
                namespace=namespace,
                dataset=dataset,
                credentials=credentials,
            )
            if not log_parsing
            else LoggingConnector(
                project=project,
                namespace=namespace,
                dataset=dataset,
                credentials=credentials,
                window=log_parsing_window,
            )
        )

    def nodes(self):
        with self.connector.connect() as conn:
            connector_nodes = conn.nodes()
            grai_nodes = adapt_to_client(connector_nodes, self.source, self.version)
        return grai_nodes

    def edges(self):
        with self.connector.connect() as conn:
            connector_edges = conn.edges()
            grai_edges = adapt_to_client(connector_edges, self.source, self.version)
        return grai_edges

    def ready(self) -> bool:
        with self.connector.connect() as _:
            pass
        return True

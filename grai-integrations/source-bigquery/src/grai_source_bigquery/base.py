from typing import List, Optional, Union

from grai_client.integrations.base import (
    GraiIntegrationImplementationV1,
    SeparateNodesAndEdgesMixin,
)

from grai_source_bigquery.adapters import adapt_to_client
from grai_source_bigquery.loader import BigqueryConnector, LoggingConnector


class BigQueryParams:
    namespace: Optional[str] = None
    project: Optional[str] = None
    dataset: Optional[Union[str, List[str]]] = None
    credentials: Optional[str] = None
    log_parsing: Optional[bool] = False
    log_parsing_window: Optional[int] = 7


class BigQueryIntegration(SeparateNodesAndEdgesMixin, GraiIntegrationImplementationV1[BigQueryParams]):
    def setup(self, params: BigQueryParams):
        self.connector = (
            BigqueryConnector(
                project=params.project,
                namespace=params.namespace,
                dataset=params.dataset,
                credentials=params.credentials,
            )
            if not params.log_parsing
            else LoggingConnector(
                project=params.project,
                namespace=params.namespace,
                dataset=params.dataset,
                credentials=params.credentials,
                window=params.log_parsing_window,
            )
        )

    def nodes(self):
        with self.connector.connect() as conn:
            connector_nodes = conn.nodes()
            grai_nodes = adapt_to_client(connector_nodes, self.source, self.client.id)
        return grai_nodes

    def edges(self):
        with self.connector.connect() as conn:
            connector_edges = conn.edges()
            grai_edges = adapt_to_client(connector_edges, self.source, self.client.id)
        return grai_edges

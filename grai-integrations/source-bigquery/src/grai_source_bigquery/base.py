from typing import List, Literal, Optional, Tuple, Union

from grai_client.endpoints.client import BaseClient
from grai_client.integrations.base import (
    GraiIntegrationImplementationV1,
    SeparateNodesAndEdgesMixin,
)
from grai_client.update import update
from grai_schemas.base import Edge, Node, Source

from grai_source_bigquery.adapters import adapt_to_client
from grai_source_bigquery.loader import BigqueryConnector, LoggingConnector


class BigQueryIntegration(GraiIntegrationImplementationV1, SeparateNodesAndEdgesMixin):
    def __init__(
        self,
        client: BaseClient,
        source_name: str,
        namespace: Optional[str] = None,
        project: Optional[str] = None,
        dataset: Optional[Union[str, List[str]]] = None,
        credentials: Optional[str] = None,
        log_parsing: Optional[bool] = False,
        log_parsing_window: Optional[int] = 7,
    ):
        super().__init__(client, source_name)

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
            grai_nodes = adapt_to_client(connector_nodes, self.source, self.client.id)
        return grai_nodes

    def edges(self):
        with self.connector.connect() as conn:
            connector_edges = conn.edges()
            grai_edges = adapt_to_client(connector_edges, self.source, self.client.id)
        return grai_edges

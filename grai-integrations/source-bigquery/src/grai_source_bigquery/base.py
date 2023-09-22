from functools import cache
from typing import List, Optional, Tuple, Union

from grai_schemas.base import Event, SourcedEdge, SourcedNode
from grai_schemas.integrations.base import GraiIntegrationImplementation
from grai_schemas.v1.source import SourceV1

from grai_source_bigquery.adapters import adapt_to_client
from grai_source_bigquery.loader import BigqueryConnector, LoggingConnector


class BigQueryIntegration(GraiIntegrationImplementation):
    """BigQuery integration.

    Attributes:
        connector: The BigQuery connector

    """

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
        """Initializes the BigQuery integration.

        Args:
            source: The Grai data source to associate with output from the integration. More information about source objects is available in the `grai_schemas` library.
            version: The Grai data version to associate with output from the integration
            namespace: The Grai namespace to associate with output from the integration
            project: GCP project id
            dataset: BigQuery Dataset Id, or multiple datasets seperated by a comma (`,`)
            credentials: JSON credentials for service account
            log_parsing: The number of days to read logs

        """
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

    @cache
    def nodes(self) -> List[SourcedNode]:
        """Return nodes from the connector."""
        with self.connector.connect() as conn:
            connector_nodes = conn.nodes()
            grai_nodes = adapt_to_client(connector_nodes, self.source, self.version)
        return grai_nodes

    @cache
    def edges(self) -> List[SourcedEdge]:
        """Return edges from the connector."""
        with self.connector.connect() as conn:
            connector_edges = conn.edges()
            grai_edges = adapt_to_client(connector_edges, self.source, self.version)
        return grai_edges

    def get_nodes_and_edges(self) -> Tuple[List[SourcedNode], List[SourcedEdge]]:
        """Return nodes and edges from the connector."""

        return self.nodes(), self.edges()

    def ready(self) -> bool:
        """Check if the connector is ready to be used."""
        with self.connector.connect() as _:
            pass
        return True

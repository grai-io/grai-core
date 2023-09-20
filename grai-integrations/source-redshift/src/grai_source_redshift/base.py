from functools import cache
from typing import List, Optional, Tuple, Union

from grai_schemas.base import SourcedEdge, SourcedNode
from grai_schemas.integrations.base import GraiIntegrationImplementation
from grai_schemas.v1.source import SourceV1

from grai_source_redshift.adapters import adapt_to_client
from grai_source_redshift.loader import RedshiftConnector


class RedshiftIntegration(GraiIntegrationImplementation):
    def __init__(
        self,
        namespace: str,
        source: SourceV1,
        version: Optional[str] = None,
        user: Optional[str] = None,
        password: Optional[str] = None,
        database: Optional[str] = None,
        host: Optional[str] = None,
        port: Optional[Union[str, int]] = None,
    ):
        super().__init__(source, version)

        self.connector = RedshiftConnector(
            user=user,
            password=password,
            database=database,
            host=host,
            port=port,
            namespace=namespace,
        )

    @cache
    def get_nodes_and_edges(self) -> Tuple[List[SourcedNode], List[SourcedEdge]]:
        with self.connector.connect() as conn:
            nodes, edges = conn.get_nodes_and_edges()

        nodes = adapt_to_client(nodes, self.source, self.version)
        edges = adapt_to_client(edges, self.source, self.version)
        return nodes, edges

    def ready(self) -> bool:
        with self.connector.connect() as _:
            pass
        return True

    def nodes(self) -> List[SourcedNode]:
        return self.get_nodes_and_edges()[0]

    def edges(self) -> List[SourcedEdge]:
        return self.get_nodes_and_edges()[1]

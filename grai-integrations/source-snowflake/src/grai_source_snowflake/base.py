from functools import cache
from typing import List, Optional, Tuple

from grai_schemas.base import SourcedEdge, SourcedNode
from grai_schemas.integrations.base import GraiIntegrationImplementation
from grai_schemas.v1.source import SourceV1

from grai_source_snowflake.adapters import adapt_to_client
from grai_source_snowflake.loader import SnowflakeConnector


class SnowflakeIntegration(GraiIntegrationImplementation):
    def __init__(
        self,
        source: SourceV1,
        version: Optional[str] = None,
        account: Optional[str] = None,
        user: Optional[str] = None,
        password: Optional[str] = None,
        warehouse: Optional[str] = None,
        role: Optional[str] = None,
        database: Optional[str] = None,
        namespace: Optional[str] = None,
        **kwargs,
    ):
        super().__init__(source, version)

        self.connector = SnowflakeConnector(
            account=account,
            user=user,
            password=password,
            warehouse=warehouse,
            role=role,
            database=database,
            namespace=namespace,
            **kwargs,
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

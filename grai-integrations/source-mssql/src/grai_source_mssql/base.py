from functools import cache
from typing import List, Optional, Tuple

from grai_schemas.base import SourcedEdge, SourcedNode
from grai_schemas.integrations.base import GraiIntegrationImplementation
from grai_schemas.v1.source import SourceV1

from grai_source_mssql.adapters import adapt_to_client
from grai_source_mssql.loader import MsSQLConnector


class MsSQLIntegration(GraiIntegrationImplementation):
    def __init__(
        self,
        source: SourceV1,
        version: Optional[str] = None,
        driver: Optional[str] = None,
        user: Optional[str] = None,
        password: Optional[str] = None,
        database: Optional[str] = None,
        server: Optional[str] = None,
        protocol: Optional[str] = None,
        host: Optional[str] = None,
        port: Optional[str] = None,
        encrypt: Optional[bool] = None,
        namespace: Optional[str] = None,
        additional_connection_strings: Optional[List[str]] = None,
    ):
        super().__init__(source, version)

        self.connector = MsSQLConnector(
            driver=driver,
            user=user,
            password=password,
            database=database,
            server=server,
            protocol=protocol,
            host=host,
            port=port,
            encrypt=encrypt,
            namespace=namespace,
            additional_connection_strings=additional_connection_strings,
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

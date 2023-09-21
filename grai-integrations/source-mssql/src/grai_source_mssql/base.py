from functools import cache
from typing import List, Optional, Tuple

from grai_schemas.base import SourcedEdge, SourcedNode
from grai_schemas.integrations.base import GraiIntegrationImplementation
from grai_schemas.v1.source import SourceV1

from grai_source_mssql.adapters import adapt_to_client
from grai_source_mssql.loader import MsSQLConnector


class MsSQLIntegration(GraiIntegrationImplementation):
    """A class for extracting Grai compliant metadata from flat files like csv and parquet.

    Attributes:
        connector: Responsible for communicating with MsSQL through odbc.

    """

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
        """Initializes the MsSQL integration.

        Args:
            source: The Grai data source to associate with output from the integration. More information about source objects is available in the `grai_schemas` library.
            version: The Grai data version to associate with output from the integration
            namespace: The Grai namespace to associate with output from the integration
            driver: The odbc driver to use when connecting to MsSQL. If not provided, a default driver available on the system will be used.
            user: The username to use when connecting to MsSQL.
            password: The password to use when connecting to MsSQL.
            database: The MsSQL database to connect to.
            server: The MsSQL server to connect to.
            protocol: The protocol to use when connecting to MsSQL.
            host: The MsSQL host address.
            port: The MsSQL port.
            encrypt: Whether or not to encrypt the connection to MsSQL.
            additional_connection_strings: A list of additional ODBC connection strings to use when connecting to MsSQL.
        """
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
        """Returns a tuple of lists of SourcedNode and SourcedEdge objects"""
        with self.connector.connect() as conn:
            nodes, edges = conn.get_nodes_and_edges()

        nodes = adapt_to_client(nodes, self.source, self.version)
        edges = adapt_to_client(edges, self.source, self.version)
        return nodes, edges

    def ready(self) -> bool:
        """Returns True if the integration is ready to run"""
        with self.connector.connect() as _:
            pass
        return True

    def nodes(self) -> List[SourcedNode]:
        """Returns a list of SourcedNode objects"""
        return self.get_nodes_and_edges()[0]

    def edges(self) -> List[SourcedEdge]:
        """Returns a list of SourcedEdge objects"""
        return self.get_nodes_and_edges()[1]

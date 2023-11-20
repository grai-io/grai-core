import re
from functools import cache
from typing import List, Optional, Tuple, Union

from grai_schemas.base import SourcedEdge, SourcedNode
from grai_schemas.integrations.base import GraiIntegrationImplementation
from grai_schemas.integrations.errors import (
    IncorrectPasswordError,
    MissingPermissionError,
    NoConnectionError,
)
from grai_schemas.v1.source import SourceV1
from psycopg2.errors import OperationalError

from grai_source_postgres.adapters import adapt_to_client
from grai_source_postgres.loader import PostgresConnector


class PostgresIntegration(GraiIntegrationImplementation):
    """A class for extracting Grai compliant metadata from Postgres

    Attributes:
        connector: The connector responsible for communicating with postgres.

    """

    def __init__(
        self,
        source: SourceV1,
        version: Optional[str] = None,
        dbname: Optional[str] = None,
        user: Optional[str] = None,
        password: Optional[str] = None,
        host: Optional[str] = None,
        port: Optional[Union[str, int]] = None,
        namespace: Optional[str] = None,
    ):
        """Initializes the Postgres integration.

        Args:
           source: The Grai data source to associate with output from the integration. More information about source objects is available in the `grai_schemas` library.
           version: The Grai data version to associate with output from the integration
           namespace: The Grai namespace to associate with output from the integration
           dbname: The Postgres database to connect to.
           user: The username to use when connecting to Postgres.
           password: The password to use when connecting to Postgres.
           host: The Postgres host address.
           port: The Postgres port.
        """
        super().__init__(source, version)

        self.connector = PostgresConnector(
            dbname=dbname,
            user=user,
            password=password,
            host=host,
            port=port,
            namespace=namespace,
        )

    def handle_error(self, err: OperationalError):
        string = str(err)

        if string.startswith("could not translate host name"):
            raise NoConnectionError(string)

        if string.startswith("connection to server at"):
            if re.search(r"FATAL:  password authentication failed for user", string):
                raise IncorrectPasswordError(string)

            if re.search(r"FATAL:  database \".*\" does not exist", string):
                raise MissingPermissionError(string)

            raise err

        raise err

    @cache
    def get_nodes_and_edges(self) -> Tuple[List[SourcedNode], List[SourcedEdge]]:
        """Returns a tuple of lists of SourcedNode and SourcedEdge objects"""
        try:
            with self.connector.connect() as conn:
                nodes, edges = conn.get_nodes_and_edges()
        except OperationalError as e:
            self.handle_error(e)

        nodes = adapt_to_client(nodes, self.source, self.version)
        edges = adapt_to_client(edges, self.source, self.version)
        return nodes, edges

    def ready(self) -> bool:
        """Returns True if the integration is ready to run"""
        try:
            with self.connector.connect() as _:
                pass
            return True
        except OperationalError as e:
            self.handle_error(e)

    def nodes(self) -> List[SourcedNode]:
        """Returns a list of SourcedNode objects"""
        return self.get_nodes_and_edges()[0]

    def edges(self) -> List[SourcedEdge]:
        """Returns a list of SourcedEdge objects"""
        return self.get_nodes_and_edges()[1]

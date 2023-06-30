from typing import Optional, Union

from grai_client.endpoints.client import BaseClient
from grai_client.integrations.base import (
    ConnectorMixin,
    GraiIntegrationImplementationV1,
)
from grai_schemas.v1.source import SourceSpec

from grai_source_mysql.adapters import adapt_to_client
from grai_source_mysql.loader import MySQLConnector


class MySQLIntegration(ConnectorMixin, GraiIntegrationImplementationV1):
    def __init__(
        self,
        client: Optional[BaseClient] = None,
        source_name: Optional[str] = None,
        source: Optional[SourceSpec] = None,
        dbname: Optional[str] = None,
        user: Optional[str] = None,
        password: Optional[str] = None,
        host: Optional[str] = None,
        port: Optional[Union[str, int]] = None,
        namespace: Optional[str] = None,
    ):
        super().__init__(client, source_name, source)

        self.connection = MySQLConnector(
            dbname=dbname,
            user=user,
            password=password,
            host=host,
            port=port,
            namespace=namespace,
        )

    def adapt_to_client(self, objects):
        return adapt_to_client(objects, self.source, self.version)

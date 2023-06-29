from typing import Optional, Union

from grai_client.endpoints.client import BaseClient
from grai_client.integrations.base import (
    ConnectorMixin,
    GraiIntegrationImplementationV1,
)

from grai_source_mysql.loader import MySQLConnector


class MySQLIntegration(GraiIntegrationImplementationV1, ConnectorMixin):
    def __init__(
        self,
        client: BaseClient,
        source_name: str,
        dbname: Optional[str] = None,
        user: Optional[str] = None,
        password: Optional[str] = None,
        host: Optional[str] = None,
        port: Optional[Union[str, int]] = None,
        namespace: Optional[str] = None,
    ):
        super().__init__(client, source_name)

        self.connection = MySQLConnector(
            dbname=dbname,
            user=user,
            password=password,
            host=host,
            port=port,
            namespace=namespace,
        )

from typing import Optional, Union

from grai_client.integrations.base import ConnectorMixin, GraiIntegrationImplementation
from grai_schemas.v1.source import SourceV1

from grai_source_postgres.adapters import adapt_to_client
from grai_source_postgres.loader import PostgresConnector


class PostgresIntegration(ConnectorMixin, GraiIntegrationImplementation):
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
        super().__init__(source, version)

        self.connector = PostgresConnector(
            dbname=dbname,
            user=user,
            password=password,
            host=host,
            port=port,
            namespace=namespace,
        )

    def adapt_to_client(self, objects):
        return adapt_to_client(objects, self.source, self.version)

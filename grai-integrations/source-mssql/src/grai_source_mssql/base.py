from typing import List, Optional

from grai_client.integrations.base import ConnectorMixin, GraiIntegrationImplementation
from grai_schemas.v1.source import SourceV1

from grai_source_mssql.adapters import adapt_to_client
from grai_source_mssql.loader import MsSQLConnector


class MsSQLIntegration(ConnectorMixin, GraiIntegrationImplementation):
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

    def adapt_to_client(self, objects):
        return adapt_to_client(objects, self.source, self.version)

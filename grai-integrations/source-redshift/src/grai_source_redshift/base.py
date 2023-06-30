from typing import Optional, Union

from grai_client.endpoints.client import BaseClient
from grai_client.integrations.base import ConnectorMixin, GraiIntegrationImplementation
from grai_schemas.v1.source import SourceSpec

from grai_source_redshift.adapters import adapt_to_client
from grai_source_redshift.loader import RedshiftConnector


class RedshiftIntegration(ConnectorMixin, GraiIntegrationImplementation):
    def __init__(
        self,
        namespace: str,
        client: Optional[BaseClient] = None,
        source_name: Optional[str] = None,
        source: Optional[SourceSpec] = None,
        user: Optional[str] = None,
        password: Optional[str] = None,
        database: Optional[str] = None,
        host: Optional[str] = None,
        port: Optional[Union[str, int]] = None,
    ):
        super().__init__(client, source_name, source)

        self.connector = RedshiftConnector(
            user=user,
            password=password,
            database=database,
            host=host,
            port=port,
            namespace=namespace,
        )

    def adapt_to_client(self, objects):
        return adapt_to_client(objects, self.source, self.version)

from typing import Optional, Union

from grai_client.endpoints.client import BaseClient
from grai_client.integrations.base import (
    ConnectorMixin,
    GraiIntegrationImplementationV1,
)

from grai_source_redshift.adapters import adapt_to_client
from grai_source_redshift.loader import RedshiftConnector


class RedshiftIntegration(ConnectorMixin, GraiIntegrationImplementationV1):
    def __init__(
        self,
        client: BaseClient,
        source_name: str,
        namespace: str,
        user: Optional[str] = None,
        password: Optional[str] = None,
        database: Optional[str] = None,
        host: Optional[str] = None,
        port: Optional[Union[str, int]] = None,
    ):
        super().__init__(client, source_name)

        self.connector = RedshiftConnector(
            user=user,
            password=password,
            database=database,
            host=host,
            port=port,
            namespace=namespace,
        )

    def adapt_to_client(self, objects):
        return adapt_to_client(objects, self.source, self.client.version)

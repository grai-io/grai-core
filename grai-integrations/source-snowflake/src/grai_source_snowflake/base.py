from typing import Optional

from grai_client.endpoints.client import BaseClient
from grai_client.integrations.base import ConnectorMixin, GraiIntegrationImplementation
from grai_schemas.v1.source import SourceSpec

from grai_source_snowflake.adapters import adapt_to_client
from grai_source_snowflake.loader import SnowflakeConnector


class SnowflakeIntegration(ConnectorMixin, GraiIntegrationImplementation):
    def __init__(
        self,
        client: Optional[BaseClient] = None,
        source_name: Optional[str] = None,
        source: Optional[SourceSpec] = None,
        account: Optional[str] = None,
        user: Optional[str] = None,
        password: Optional[str] = None,
        warehouse: Optional[str] = None,
        role: Optional[str] = None,
        database: Optional[str] = None,
        namespace: Optional[str] = None,
        **kwargs,
    ):
        super().__init__(client, source_name, source)

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

    def adapt_to_client(self, objects):
        return adapt_to_client(objects, self.source, self.version)

from typing import Optional

from grai_client.endpoints.client import BaseClient
from grai_client.integrations.base import (
    ConnectorMixin,
    GraiIntegrationImplementationV1,
)

from grai_source_snowflake.adapters import adapt_to_client
from grai_source_snowflake.loader import SnowflakeConnector


class SnowflakeIntegration(ConnectorMixin, GraiIntegrationImplementationV1):
    def __init__(
        self,
        client: BaseClient,
        source_name: str,
        account: Optional[str] = None,
        user: Optional[str] = None,
        password: Optional[str] = None,
        warehouse: Optional[str] = None,
        role: Optional[str] = None,
        database: Optional[str] = None,
        namespace: Optional[str] = None,
        **kwargs,
    ):
        super().__init__(client, source_name)

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
        return adapt_to_client(objects, self.source, self.client.id)

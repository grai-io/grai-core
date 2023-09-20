from grai_schemas.v1.source import SourceV1

from .base import IntegrationAdapter
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from grai_source_mssql.base import MsSQLIntegration


class MssqlAdapter(IntegrationAdapter):
    def get_integration(self) -> "MsSQLIntegration":
        from grai_source_mssql.base import MsSQLIntegration

        metadata = self.run.connection.metadata
        secrets = self.run.connection.secrets
        source = SourceV1.from_spec(
            {
                "id": self.run.source.id,
                "name": self.run.source.name,
            }
        )
        integration = MsSQLIntegration(
            source=source,
            user=metadata.get("user"),
            password=secrets.get("password"),
            database=metadata.get("database"),
            host=metadata.get("host"),
            port=metadata.get("port"),
            driver=metadata.get("driver"),
            namespace=self.run.connection.namespace,
            additional_connection_strings=["TrustServerCertificate=yes"],
        )
        return integration

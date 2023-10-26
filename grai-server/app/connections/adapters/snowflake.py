from grai_schemas.v1.source import SourceV1
from grai_source_snowflake.base import SnowflakeIntegration

from .base import IntegrationAdapter


class SnowflakeAdapter(IntegrationAdapter):
    def get_integration(self) -> SnowflakeIntegration:
        metadata = self.run.connection.metadata
        secrets = self.run.connection.secrets
        source = SourceV1.from_spec(
            {
                "id": self.run.source.id,
                "name": self.run.source.name,
            }
        )
        integration = SnowflakeIntegration(
            source=source,
            account=metadata.get("account"),
            user=metadata.get("user"),
            password=secrets.get("password"),
            role=metadata["role"],
            warehouse=metadata.get("warehouse"),
            database=metadata.get("database"),
            namespace=self.run.connection.namespace,
        )
        return integration

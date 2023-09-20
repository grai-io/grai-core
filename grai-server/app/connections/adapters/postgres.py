from grai_source_postgres.base import PostgresIntegration
from grai_schemas.v1.source import SourceV1

from .base import IntegrationAdapter


class PostgresAdapter(IntegrationAdapter):
    def get_integration(self) -> PostgresIntegration:
        metadata = self.run.connection.metadata
        secrets = self.run.connection.secrets
        source = SourceV1.from_spec(
            {
                "id": self.run.source.id,
                "name": self.run.source.name,
            }
        )
        integration = PostgresIntegration(
            source=source,
            dbname=metadata["dbname"],
            user=metadata["user"],
            password=secrets["password"],
            host=metadata["host"],
            port=metadata["port"],
            namespace=self.run.connection.namespace,
        )
        return integration

from .base import BaseAdapter
from grai_schemas.v1.source import SourceV1
from grai_schemas.integrations.base import ValidatedIntegration


class MssqlAdapter(BaseAdapter):
    def get_integration(self) -> ValidatedIntegration:
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
        return ValidatedIntegration(integration)

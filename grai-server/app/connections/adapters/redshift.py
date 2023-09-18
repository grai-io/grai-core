from grai_schemas.integrations.base import ValidatedIntegration
from grai_schemas.v1.source import SourceV1

from .base import IntegrationAdapter


class RedshiftAdapter(IntegrationAdapter):
    def get_integration(self) -> ValidatedIntegration:
        from grai_source_redshift.base import RedshiftIntegration

        metadata = self.run.connection.metadata
        secrets = self.run.connection.secrets
        source = SourceV1.from_spec(
            {
                "id": self.run.source.id,
                "name": self.run.source.name,
            }
        )
        integration = RedshiftIntegration(
            source=source,
            host=metadata["host"],
            port=metadata["port"],
            database=metadata["database"],
            user=metadata["user"],
            password=secrets["password"],
            namespace=self.run.connection.namespace,
        )
        return ValidatedIntegration(integration)

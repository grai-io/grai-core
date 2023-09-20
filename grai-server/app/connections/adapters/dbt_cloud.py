from grai_schemas.v1.source import SourceV1
from grai_source_dbt_cloud.base import DbtCloudIntegration
from .base import IntegrationAdapter


class DbtCloudAdapter(IntegrationAdapter):
    def get_integration(self) -> DbtCloudIntegration:
        secrets = self.run.connection.secrets
        namespace = self.run.connection.namespace
        source = SourceV1.from_spec(
            {
                "id": self.run.source.id,
                "name": self.run.source.name,
            }
        )
        integration = DbtCloudIntegration(
            source=source,
            api_key=secrets["api_key"],
            namespace=namespace,
        )

        return integration

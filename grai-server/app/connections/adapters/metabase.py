from grai_schemas.integrations.base import ValidatedIntegration
from grai_schemas.v1.source import SourceV1

from .base import IntegrationAdapter


class MetabaseAdapter(IntegrationAdapter):
    def get_integration(self) -> ValidatedIntegration:
        from grai_source_metabase.base import MetabaseIntegration

        metadata = self.run.connection.metadata
        secrets = self.run.connection.secrets
        source = SourceV1.from_spec(
            {
                "id": self.run.source.id,
                "name": self.run.source.name,
            }
        )
        integration = MetabaseIntegration(
            source=source,
            username=metadata.get("username"),
            password=secrets.get("password"),
            namespace_map=metadata.get("namespaces") if metadata.get("namespaces") != "" else None,
            metabase_namespace=self.run.connection.namespace,
            endpoint=metadata.get("endpoint"),
        )
        return ValidatedIntegration(integration)

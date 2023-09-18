import json

from grai_source_looker.base import LookerIntegration
from grai_schemas.v1.source import SourceV1

from .base import IntegrationAdapter


class LookerAdapter(IntegrationAdapter):
    def get_integration(self) -> LookerIntegration:
        metadata = self.run.connection.metadata
        secrets = self.run.connection.secrets
        source = SourceV1.from_spec(
            {
                "id": self.run.source.id,
                "name": self.run.source.name,
            }
        )
        integration = LookerIntegration(
            source=source,
            base_url=metadata["base_url"],
            client_id=metadata["client_id"],
            client_secret=secrets["client_secret"],
            namespace=self.run.connection.namespace,
            namespaces=json.loads(metadata["namespaces"]) if metadata.get("namespaces") else None,
        )
        return integration

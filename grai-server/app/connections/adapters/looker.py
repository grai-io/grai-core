import json

from .base import BaseAdapter
from grai_schemas.v1.source import SourceV1
from grai_schemas.integrations.base import ValidatedIntegration


class LookerAdapter(BaseAdapter):
    def get_integration(self) -> ValidatedIntegration:
        from grai_source_looker.base import LookerIntegration

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
        return ValidatedIntegration(integration)

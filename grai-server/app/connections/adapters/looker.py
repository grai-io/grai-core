from .base import BaseAdapter
import json


class LookerAdapter(BaseAdapter):
    def get_integration(self):
        from grai_source_looker.base import LookerIntegration

        metadata = self.run.connection.metadata
        secrets = self.run.connection.secrets

        return LookerIntegration(
            source={
                "id": self.run.source.id,
                "name": self.run.source.name,
            },
            base_url=metadata["base_url"],
            client_id=metadata["client_id"],
            client_secret=secrets["client_secret"],
            namespace=self.run.connection.namespace,
            namespaces=json.loads(metadata["namespaces"]) if metadata.get("namespaces") else None,
        )

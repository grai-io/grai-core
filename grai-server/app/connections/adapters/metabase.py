from .base import BaseAdapter
from grai_schemas.v1.source import SourceV1


class MetabaseAdapter(BaseAdapter):
    def get_integration(self):
        from grai_source_metabase.base import MetabaseIntegration

        metadata = self.run.connection.metadata
        secrets = self.run.connection.secrets
        source = SourceV1.from_spec(
            {
                "id": self.run.source.id,
                "name": self.run.source.name,
            }
        )
        return MetabaseIntegration(
            source=source,
            username=metadata.get("username"),
            password=secrets.get("password"),
            namespace_map=metadata.get("namespaces") if metadata.get("namespaces") != "" else None,
            metabase_namespace=self.run.connection.namespace,
            endpoint=metadata.get("endpoint"),
        )

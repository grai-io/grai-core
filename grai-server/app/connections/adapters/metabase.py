from .base import BaseAdapter


class MetabaseAdapter(BaseAdapter):
    def get_integration(self):
        from grai_source_metabase.base import MetabaseIntegration

        metadata = self.run.connection.metadata
        secrets = self.run.connection.secrets

        return MetabaseIntegration(
            source={
                "id": self.run.source.id,
                "name": self.run.source.name,
            },
            username=metadata.get("username"),
            password=secrets.get("password"),
            namespace_map=metadata.get("namespaces"),
            metabase_namespace=self.run.connection.namespace,
            endpoint=metadata.get("endpoint"),
        )

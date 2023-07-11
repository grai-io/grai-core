from .base import BaseAdapter


class MetabaseAdapter(BaseAdapter):
    def get_nodes_and_edges(self):
        from grai_source_metabase.base import MetabaseIntegration

        metadata = self.run.connection.metadata
        secrets = self.run.connection.secrets

        return MetabaseIntegration(
            username=metadata.get("username"),
            password=secrets.get("password"),
            namespaces=metadata.get("namespaces"),
            metabase_namespace=self.run.connection.namespace,
            endpoint=metadata.get("endpoint"),
        )

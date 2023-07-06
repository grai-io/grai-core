from .base import BaseAdapter


class MetabaseAdapter(BaseAdapter):
    def get_nodes_and_edges(self):
        from grai_source_metabase.base import get_nodes_and_edges
        from grai_source_metabase.loader import MetabaseConnector

        metadata = self.run.connection.metadata
        secrets = self.run.connection.secrets

        conn = MetabaseConnector(
            username=metadata.get("username"),
            password=secrets.get("password"),
            namespaces=metadata.get("namespaces"),
            metabase_namespace=self.run.connection.namespace,
            endpoint=metadata.get("endpoint"),
        )

        return get_nodes_and_edges(conn, "v1")

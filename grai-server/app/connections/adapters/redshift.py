from .base import BaseAdapter


class RedshiftAdapter(BaseAdapter):
    def get_nodes_and_edges(self):
        from grai_source_redshift.base import get_nodes_and_edges
        from grai_source_redshift.loader import RedshiftConnector

        metadata = self.run.connection.metadata
        secrets = self.run.connection.secrets

        conn = RedshiftConnector(
            host=metadata["host"],
            port=metadata["port"],
            database=metadata["database"],
            user=metadata["user"],
            password=secrets["password"],
            namespace=self.run.connection.namespace,
        )

        return get_nodes_and_edges(conn, "v1")

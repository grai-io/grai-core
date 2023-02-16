from .base import BaseAdapter


class PostgresAdapter(BaseAdapter):
    def get_nodes_and_edges(self):
        from grai_source_postgres.base import get_nodes_and_edges
        from grai_source_postgres.loader import PostgresConnector

        metadata = self.run.connection.metadata
        secrets = self.run.connection.secrets

        conn = PostgresConnector(
            host=metadata["host"],
            port=metadata["port"],
            dbname=metadata["dbname"],
            user=metadata["user"],
            password=secrets["password"],
            namespace=self.run.connection.namespace,
        )

        return get_nodes_and_edges(conn, "v1")

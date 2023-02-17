from .base import BaseAdapter


class MySQLAdapter(BaseAdapter):
    def get_nodes_and_edges(self):
        from grai_source_mysql.base import get_nodes_and_edges
        from grai_source_mysql.loader import MySQLConnector

        metadata = self.run.connection.metadata
        secrets = self.run.connection.secrets

        conn = MySQLConnector(
            host=metadata["host"],
            port=metadata["port"],
            dbname=metadata["dbname"],
            user=metadata["user"],
            password=secrets["password"],
            namespace=self.run.connection.namespace,
        )

        return get_nodes_and_edges(conn, "v1")

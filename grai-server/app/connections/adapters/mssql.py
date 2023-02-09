from .base import BaseAdapter


class MssqlAdapter(BaseAdapter):
    def get_nodes_and_edges(self):
        from grai_source_mssql.base import get_nodes_and_edges
        from grai_source_mssql.loader import MsSQLConnector

        metadata = self.run.connection.metadata
        secrets = self.run.connection.secrets

        conn = MsSQLConnector(
            user=metadata.get("user"),
            password=secrets.get("password"),
            database=metadata.get("database"),
            host=metadata.get("host"),
            port=metadata.get("port"),
            namespace=self.run.connection.namespace,
            additional_connection_strings=["TrustServerCertificate=yes"],
        )

        return get_nodes_and_edges(conn, "v1")

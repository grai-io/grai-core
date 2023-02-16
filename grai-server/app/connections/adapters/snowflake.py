from .base import BaseAdapter


class SnowflakeAdapter(BaseAdapter):
    def get_nodes_and_edges(self):
        from grai_source_snowflake.base import get_nodes_and_edges
        from grai_source_snowflake.loader import SnowflakeConnector

        metadata = self.run.connection.metadata
        secrets = self.run.connection.secrets

        conn = SnowflakeConnector(
            account=metadata.get("account"),
            user=metadata.get("user"),
            password=secrets.get("password"),
            role=metadata["role"],
            warehouse=metadata.get("warehouse"),
            database=metadata.get("database"),
            schema=metadata.get("schema"),
            namespace=self.run.connection.namespace,
        )

        return get_nodes_and_edges(conn, "v1")

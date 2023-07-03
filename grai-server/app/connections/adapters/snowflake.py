from .base import BaseAdapter


class SnowflakeAdapter(BaseAdapter):
    def get_integration(self):
        from grai_source_snowflake.base import SnowflakeIntegration

        metadata = self.run.connection.metadata
        secrets = self.run.connection.secrets

        return SnowflakeIntegration(
            source={
                "id": self.run.source.id,
                "name": self.run.source.name,
            },
            account=metadata.get("account"),
            user=metadata.get("user"),
            password=secrets.get("password"),
            role=metadata["role"],
            warehouse=metadata.get("warehouse"),
            database=metadata.get("database"),
            namespace=self.run.connection.namespace,
        )

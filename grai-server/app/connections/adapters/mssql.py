from .base import BaseAdapter


class MssqlAdapter(BaseAdapter):
    def get_integration(self):
        from grai_source_mssql.base import MsSQLIntegration

        metadata = self.run.connection.metadata
        secrets = self.run.connection.secrets

        return MsSQLIntegration(
            source={
                "id": self.run.source.id,
                "name": self.run.source.name,
            },
            user=metadata.get("user"),
            password=secrets.get("password"),
            database=metadata.get("database"),
            host=metadata.get("host"),
            port=metadata.get("port"),
            driver=metadata.get("driver"),
            namespace=self.run.connection.namespace,
            additional_connection_strings=["TrustServerCertificate=yes"],
        )

from .base import BaseAdapter


class PostgresAdapter(BaseAdapter):
    def get_integration(self):
        from grai_source_postgres.base import PostgresIntegration

        metadata = self.run.connection.metadata
        secrets = self.run.connection.secrets

        return PostgresIntegration(
            source={
                "id": self.run.source.id,
                "name": self.run.source.name,
            },
            dbname=metadata["dbname"],
            user=metadata["user"],
            password=secrets["password"],
            host=metadata["host"],
            port=metadata["port"],
            namespace=self.run.connection.namespace,
        )

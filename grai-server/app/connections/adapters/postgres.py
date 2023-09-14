from .base import BaseAdapter
from grai_schemas.v1.source import SourceV1


class PostgresAdapter(BaseAdapter):
    def get_integration(self):
        from grai_source_postgres.base import PostgresIntegration

        metadata = self.run.connection.metadata
        secrets = self.run.connection.secrets
        source = SourceV1.from_spec(
            {
                "id": self.run.source.id,
                "name": self.run.source.name,
            }
        )
        return PostgresIntegration(
            source=source,
            dbname=metadata["dbname"],
            user=metadata["user"],
            password=secrets["password"],
            host=metadata["host"],
            port=metadata["port"],
            namespace=self.run.connection.namespace,
        )

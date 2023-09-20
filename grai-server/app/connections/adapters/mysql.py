from grai_source_mysql.base import MySQLIntegration
from grai_schemas.v1.source import SourceV1

from .base import IntegrationAdapter


class MySQLAdapter(IntegrationAdapter):
    def get_integration(self) -> MySQLIntegration:
        metadata = self.run.connection.metadata
        secrets = self.run.connection.secrets
        source = SourceV1.from_spec(
            {
                "id": self.run.source.id,
                "name": self.run.source.name,
            }
        )
        integration = MySQLIntegration(
            source=source,
            host=metadata["host"],
            port=metadata["port"],
            dbname=metadata["dbname"],
            user=metadata["user"],
            password=secrets["password"],
            namespace=self.run.connection.namespace,
        )
        return integration

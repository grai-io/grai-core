from .base import BaseAdapter
from grai_schemas.v1.source import SourceV1
from grai_schemas.integrations.base import ValidatedIntegration


class MySQLAdapter(BaseAdapter):
    def get_integration(self) -> ValidatedIntegration:
        from grai_source_mysql.base import MySQLIntegration

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
        return ValidatedIntegration(integration)

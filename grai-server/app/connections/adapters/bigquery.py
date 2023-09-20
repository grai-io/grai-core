from grai_schemas.v1.source import SourceV1
from grai_source_bigquery.base import BigQueryIntegration

from .base import IntegrationAdapter


class BigqueryAdapter(IntegrationAdapter):
    def get_integration(self) -> BigQueryIntegration:
        metadata = self.run.connection.metadata
        secrets = self.run.connection.secrets
        source_spec = {
            "id": self.run.source.id,
            "name": self.run.source.name,
            "workspace": self.run.workspace.id,
        }
        integration = BigQueryIntegration(
            SourceV1.from_spec(source_spec),
            namespace=self.run.connection.namespace,
            project=metadata.get("project"),
            dataset=metadata.get("dataset").split(","),
            credentials=secrets.get("credentials"),
            log_parsing=metadata.get("log_parsing", False),
            log_parsing_window=int(metadata.get("log_parsing_window", 7)),
        )
        return integration

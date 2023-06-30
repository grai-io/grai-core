from .base import BaseAdapter
from grai_schemas.v1.source import SourceV1


class BigqueryAdapter(BaseAdapter):
    def get_integration(self):
        from grai_source_bigquery.base import BigQueryIntegration

        metadata = self.run.connection.metadata
        secrets = self.run.connection.secrets

        return BigQueryIntegration(
            {
                "id": self.run.source.id,
                "name": self.run.source.name,
            },
            namespace=self.run.connection.namespace,
            project=metadata.get("project"),
            dataset=metadata.get("dataset").split(","),
            credentials=secrets.get("credentials"),
            log_parsing=metadata.get("log_parsing", False),
            log_parsing_window=int(metadata.get("log_parsing_window", 7)),
        )

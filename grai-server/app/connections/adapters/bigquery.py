from .base import BaseAdapter


class BigqueryAdapter(BaseAdapter):
    def get_nodes_and_edges(self):
        from grai_source_bigquery.base import get_nodes_and_edges
        from grai_source_bigquery.loader import BigqueryConnector

        metadata = self.run.connection.metadata
        secrets = self.run.connection.secrets

        conn = BigqueryConnector(
            project=metadata.get("project"),
            dataset=metadata.get("dataset"),
            credentials=secrets.get("credentials"),
            namespace=self.run.connection.namespace,
        )

        return get_nodes_and_edges(conn, "v1")

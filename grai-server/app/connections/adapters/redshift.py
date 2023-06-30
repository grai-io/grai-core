from .base import BaseAdapter


class RedshiftAdapter(BaseAdapter):
    def get_nodes_and_edges(self):
        from grai_source_redshift.base import RedshiftIntegration

        metadata = self.run.connection.metadata
        secrets = self.run.connection.secrets

        return RedshiftIntegration(
            source={
                "id": self.run.source.id,
                "name": self.run.source.name,
            },
            host=metadata["host"],
            port=metadata["port"],
            database=metadata["database"],
            user=metadata["user"],
            password=secrets["password"],
            namespace=self.run.connection.namespace,
        )

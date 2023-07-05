from .base import BaseAdapter


class DbtCloudAdapter(BaseAdapter):
    def get_integration(self):
        from grai_source_dbt_cloud.base import DbtCloudIntegration
        from grai_schemas.v1.source import SourceV1

        secrets = self.run.connection.secrets
        namespace = self.run.connection.namespace

        return DbtCloudIntegration(
            source=SourceV1.from_spec(
                {
                    "id": self.run.source.id,
                    "name": self.run.source.name,
                }
            ),
            api_key=secrets["api_key"],
            namespace=namespace,
        )

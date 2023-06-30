from .base import BaseAdapter
from grai_source_dbt_cloud.base import DbtCloudIntegration


class DbtCloudAdapter(BaseAdapter):
    def get_intergration(self):
        secrets = self.run.connection.secrets
        namespace = self.run.connection.namespace

        return DbtCloudIntegration(
            source={
                "id": self.run.source.id,
                "name": self.run.source.name,
            },
            api_key=secrets["api_key"],
            namespace=namespace,
        )

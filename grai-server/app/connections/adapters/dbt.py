import json

from grai_schemas.v1.source import SourceV1
from grai_source_dbt.base import DbtIntegration

from .base import IntegrationAdapter


class DbtAdapter(IntegrationAdapter):
    def get_integration(self) -> DbtIntegration:
        namespace = self.run.connection.namespace
        run_file = self.run.files.first()

        with run_file.file.open("r") as f:
            manifest_obj = json.load(f)

        source = SourceV1.from_spec(
            {
                "id": self.run.source.id,
                "name": self.run.source.name,
            }
        )
        integration = DbtIntegration(manifest_obj, source=source, namespace=namespace)
        return integration

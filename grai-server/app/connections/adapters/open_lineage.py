import json

from grai_schemas.v1.source import SourceV1
from grai_source_openlineage.base import OpenLineageIntegration

from .base import IntegrationAdapter


class OpenLineageAdapter(IntegrationAdapter):
    def get_integration(self) -> OpenLineageIntegration:
        namespace = self.run.connection.namespace

        source = SourceV1.from_spec(
            {
                "id": self.run.source.id,
                "name": self.run.source.name,
            }
        )
        integration = OpenLineageIntegration(self.run.input, source=source, namespace=namespace)
        return integration

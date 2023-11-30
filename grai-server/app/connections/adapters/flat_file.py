import json
import os.path

from grai_schemas.v1.source import SourceV1
from grai_source_flat_file.base import FlatFileIntegration

from .base import IntegrationAdapter


class FlatFileAdapter(IntegrationAdapter):
    def get_integration(self) -> FlatFileIntegration:
        namespace = self.run.connection.namespace
        run_file = self.run.files.first().file
        table_name, extension = os.path.splitext(run_file.name)

        source = SourceV1.from_spec(
            {
                "id": self.run.source.id,
                "name": self.run.source.name,
            }
        )

        integration = FlatFileIntegration(
            run_file,
            table_name=table_name,
            file_ext=extension,
            file_location=run_file.name,
            source=source,
            namespace=namespace,
        )
        return integration

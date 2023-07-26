from connections.models import Run

from .base import BaseAdapter


class DbtAdapter(BaseAdapter):
    def get_nodes_and_edges(self):
        import json

        from grai_schemas.v1.source import SourceV1
        from grai_source_dbt.processor import ManifestProcessor

        namespace = self.run.connection.namespace

        runFile = self.run.files.first()

        with runFile.file.open("r") as f:
            manifest_obj = json.load(f)

        manifest = ManifestProcessor.load(
            manifest_obj,
            namespace,
            SourceV1.from_spec(
                {
                    "id": self.run.source.id,
                    "name": self.run.source.name,
                }
            ),
        )
        return manifest.adapted_nodes, manifest.adapted_edges

    def run_validate(self, run: Run) -> bool:
        self.run = run

        self.get_nodes_and_edges()

        return True

from .base import BaseAdapter


class DbtAdapter(BaseAdapter):
    def get_nodes_and_edges(self):
        import json

        from grai_source_dbt.processor import ManifestProcessor
        from grai_schemas.v1.source import SourceV1

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

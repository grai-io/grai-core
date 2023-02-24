from .base import BaseAdapter


class DbtAdapter(BaseAdapter):
    def get_nodes_and_edges(self):
        import json

        from grai_source_dbt.processor import ManifestProcessor

        namespace = self.run.connection.namespace

        runFile = self.run.files.first()

        with runFile.file.open("r") as f:
            manifest_obj = json.load(f)

        manifest = ManifestProcessor.load(manifest_obj, namespace)
        return manifest.adapted_nodes, manifest.adapted_edges

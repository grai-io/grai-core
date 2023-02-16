from .base import BaseAdapter


class DbtAdapter(BaseAdapter):
    def get_nodes_and_edges(self):
        import json

        from grai_source_dbt.adapters import adapt_to_client
        from grai_source_dbt.loader import DBTGraph, Manifest

        runFile = self.run.files.first()

        namespace = "default"

        # nodes, edges = get_nodes_and_edges(manifest_file=runFile.file.read(), namespace=namespace, version="v1")
        with runFile.file.open("r") as f:
            data = json.load(f)

        manifest = Manifest(**data)
        dbt_graph = DBTGraph(manifest, namespace=namespace)

        nodes = adapt_to_client(dbt_graph.nodes, "v1")
        edges = adapt_to_client(dbt_graph.edges, "v1")

        return nodes, edges

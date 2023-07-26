from query_chunk import chunk

from lineage.models import Edge, Node

from .graph_cache import GraphCache


class ExtendedGraphCache(GraphCache):
    def build_cache(self):
        for node in chunk(Node.objects.filter(workspace_id=self.workspace_id), 10000):
            self.cache_node(node)

        for edge in chunk(Edge.objects.filter(workspace_id=self.workspace_id), 10000):
            self.cache_edge(edge)

    def clear_cache(self):
        self.manager.delete(f"lineage:{self.workspace_id}")

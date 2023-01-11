from grai_client.endpoints import list_clients
from grai_client.endpoints.client import BaseClient

from grai_graph.graph import build_graph


def graph_builder(self: BaseClient):
    nodes = self.get("nodes")
    edges = self.get("edges")
    return build_graph(nodes, edges, self.id)


for client in list_clients():
    client.build_graph = graph_builder

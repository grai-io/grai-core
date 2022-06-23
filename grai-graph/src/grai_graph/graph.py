import networkx as nx


class GraphManifest:
    def __init__(self, nodes, edges):
        self.nodes = nodes
        self.edges = edges


class Graph(nx.DiGraph):
    def __init__(self, manifest):
        self.manifest = manifest

        super().__init__()
        self.add_nodes_from(self.manifest.nodes)
        self.add_edges_from(self.manifest.edges)


def build_graph(nodes, edges):
    manifest = GraphManifest(nodes, edges)
    return Graph(manifest)

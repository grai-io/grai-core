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

    def downstream_nodes(node_id):
        return nx.bfs_successors(G, node_id)
    
    def changed_nodes(node_id):
        return 

def build_graph(nodes, edges):
    manifest = GraphManifest(nodes, edges)
    return Graph(manifest)
    

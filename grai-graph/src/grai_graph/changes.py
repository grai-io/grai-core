import networkx as nx


class LineageUpdate:
    pass


def get_affected_nodes_on_delete(graph, node_id):
    return list(nx.bfs_successors(graph, node_id))


def get_affected_nodes_on_modify(graph, node_id, new_node):
    return

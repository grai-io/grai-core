import unittest
import uuid

import networkx as nx
from grai_client.testing.schema import (
    mock_v1_edge,
    mock_v1_edge_and_nodes,
    mock_v1_node,
)
from grai_schemas.models import ColumnToColumnAttributes

from grai_graph import graph
from grai_graph.test_utils import (
    DEFAULT_NAMESPACE,
    TestNodeObj,
    build_graph_from_map,
    get_analysis_from_map,
)


def get_node_id(node):
    return {"name": node.name, "namespace": node.namespace}


def test_v1_build_graph():
    edges = []
    nodes = []
    for i in range(4):
        e, n = mock_v1_edge_and_nodes()
        edges.append(e)
        nodes.extend(n)
    G = graph.build_graph(nodes, edges, "v1")
    assert isinstance(G.graph, nx.DiGraph)


class TestUniqueness(unittest.TestCase):
    preserves_unique = ColumnToColumnAttributes(preserves_unique=True)
    violates_unique = ColumnToColumnAttributes(preserves_unique=False)
    unknown_unique = ColumnToColumnAttributes()

    def test_unique_no_node_information(self):
        mock_structure = {
            "A": {self.preserves_unique: ["B"]},
            "B": {self.preserves_unique: ["C"]},
            "C": {},
        }
        G = get_analysis_from_map(mock_structure)
        results = G.test_unique_violations(
            name="A", namespace=DEFAULT_NAMESPACE, expects_unique=True
        )
        assert len(results) == 0

    def test_unique_no_node_information(self):
        mock_structure = {
            TestNodeObj(name="A", node_attributes={"is_unique": True}): {
                self.preserves_unique: ["B"]
            },
            "B": {self.preserves_unique: ["C"]},
            "C": {},
        }
        G = get_analysis_from_map(mock_structure)
        results = G.test_unique_violations(
            name="A", namespace=DEFAULT_NAMESPACE, expects_unique=False
        )
        assert len(results) == 1, results

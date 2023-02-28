import unittest
import uuid

import networkx as nx
from grai_client.testing.schema import (
    mock_v1_edge,
    mock_v1_edge_and_nodes,
    mock_v1_node,
)
from grai_schemas.v1.metadata.edges import (
    ColumnToColumnAttributes,
    TableToColumnAttributes,
    TableToTableAttributes,
)

from grai_graph import graph
from grai_graph.utils import (
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

    def get_nodes(n: int = 3):
        variables = "abcdefghijklmnopqrstuvwxyz"
        extra_kwargs = {char: TestNodeObj(name=char, node_attributes={}) for char in variables[0:n]}

        def inner(fn):
            def wraps(*args, **kwargs):
                return fn(*args, **kwargs, **extra_kwargs)

            return wraps

        return inner

    @get_nodes(n=2)
    def test_table_to_column_information(self, a, b):
        """We don't know anything about node nullableness to evaluate failure or success"""
        mock_structure = {
            a: [("b", TableToColumnAttributes())],
            b: [],
        }
        G = get_analysis_from_map(mock_structure)
        results = G.test_unique_violations(name="a", namespace=DEFAULT_NAMESPACE, expects_unique=True)
        assert len(results) == 0

    @get_nodes(n=2)
    def test_table_to_table_information(self, a, b):
        """We don't know anything about node nullableness to evaluate failure or success"""
        mock_structure = {
            a: [("b", TableToTableAttributes())],
            b: [],
        }
        G = get_analysis_from_map(mock_structure)
        results = G.test_unique_violations(name="a", namespace=DEFAULT_NAMESPACE, expects_unique=True)
        assert len(results) == 0

    @get_nodes(n=3)
    def test_no_node_information(self, a, b, c):
        """We don't know anything about node uniqueness to evaluate failure or success"""
        mock_structure = {
            a: [("b", self.preserves_unique)],
            b: [("c", self.preserves_unique)],
            c: [],
        }
        G = get_analysis_from_map(mock_structure)
        results = G.test_unique_violations(name="a", namespace=DEFAULT_NAMESPACE, expects_unique=True)
        assert len(results) == 0

    @get_nodes(n=3)
    def test_violates_unique(self, a, b, c):
        """If the edge doesn't preserve unique we can't say with certainty whether the test ought to fail"""
        a.node_attributes.is_unique = True
        mock_structure = {
            a: [("b", self.violates_unique)],
            b: [("c", self.violates_unique)],
            c: [],
        }
        G = get_analysis_from_map(mock_structure)
        results = G.test_unique_violations(name="a", namespace=DEFAULT_NAMESPACE, expects_unique=True)
        assert len(results) == 0

    # @get_nodes(n=3)
    # def test_violates_self_information(self, a, b, c):
    #     """If the initial node expect expects different uniqueness it should be identified"""
    #     a.node_attributes.is_unique = True
    #     mock_structure = {
    #         a: [("b", self.preserves_unique)],
    #         b: [("c", self.preserves_unique)],
    #         c: [],
    #     }
    #     G = get_analysis_from_map(mock_structure)
    #     results = G.test_unique_violations(name="a", namespace=DEFAULT_NAMESPACE, expects_unique=False)
    #
    #     assert len(results) == 1 and results[0][0][-1].spec.name is "a", results

    @get_nodes(n=4)
    def test_skip_violation(self, a, b, c, d):
        """Test failures should be detected even multiple jumps from the source node"""
        d.node_attributes.is_unique = False
        mock_structure = {
            a: [("b", self.preserves_unique)],
            b: [("c", self.preserves_unique)],
            c: [("d", self.preserves_unique)],
            d: [],
        }
        G = get_analysis_from_map(mock_structure)
        results = G.test_unique_violations(name="a", namespace=DEFAULT_NAMESPACE, expects_unique=True)
        assert len(results) == 1 and results[0][0][-1].spec.name is "d", results

    @get_nodes(n=3)
    def test_triangle_violation(self, a, b, c):
        """Tests ought to be able to fail following multiple different paths through lineage"""
        c.node_attributes.is_unique = False
        mock_structure = {
            a: [("b", self.preserves_unique), ("c", self.preserves_unique)],
            b: [("c", self.preserves_unique)],
            c: [],
        }
        G = get_analysis_from_map(mock_structure)
        results = G.test_unique_violations(name="a", namespace=DEFAULT_NAMESPACE, expects_unique=True)
        assert len(results) == 2 and results[0][0][-1].spec.name is "c" and results[1][0][-1].spec.name is "c"


class TestNullable(unittest.TestCase):
    preserves_nullable = ColumnToColumnAttributes(preserves_nullable=True)
    violates_nullable = ColumnToColumnAttributes(preserves_nullable=False)
    unknown_nullable = ColumnToColumnAttributes()

    def get_nodes(n: int = 3):
        variables = "abcdefghijklmnopqrstuvwxyz"
        extra_kwargs = {char: TestNodeObj(name=char, node_attributes={}) for char in variables[0:n]}

        def inner(fn):
            def wraps(*args, **kwargs):
                return fn(*args, **kwargs, **extra_kwargs)

            return wraps

        return inner

    @get_nodes(n=2)
    def test_table_to_column_information(self, a, b):
        """We don't know anything about node nullableness to evaluate failure or success"""
        mock_structure = {
            a: [("b", TableToColumnAttributes())],
            b: [],
        }
        G = get_analysis_from_map(mock_structure)
        results = G.test_nullable_violations(name="a", namespace=DEFAULT_NAMESPACE, is_nullable=True)
        assert len(results) == 0

    @get_nodes(n=2)
    def test_table_to_table_information(self, a, b):
        """We don't know anything about node nullableness to evaluate failure or success"""
        mock_structure = {
            a: [("b", TableToTableAttributes())],
            b: [],
        }
        G = get_analysis_from_map(mock_structure)
        results = G.test_nullable_violations(name="a", namespace=DEFAULT_NAMESPACE, is_nullable=True)
        assert len(results) == 0

    @get_nodes(n=3)
    def test_no_node_information(self, a, b, c):
        """We don't know anything about node nullableness to evaluate failure or success"""
        mock_structure = {
            a: [("b", self.preserves_nullable)],
            b: [("c", self.preserves_nullable)],
            c: [],
        }
        G = get_analysis_from_map(mock_structure)
        results = G.test_nullable_violations(name="a", namespace=DEFAULT_NAMESPACE, is_nullable=True)
        assert len(results) == 0

    @get_nodes(n=3)
    def test_no_node_or_edge_information(self, a, b, c):
        """We don't know anything about node nullableness to evaluate failure or success"""
        mock_structure = {
            a: [("b", self.unknown_nullable)],
            b: [("c", self.unknown_nullable)],
            c: [],
        }
        G = get_analysis_from_map(mock_structure)
        results = G.test_nullable_violations(name="a", namespace=DEFAULT_NAMESPACE, is_nullable=True)
        assert len(results) == 0

    @get_nodes(n=3)
    def test_violates_nullable(self, a, b, c):
        """If the edge doesn't preserve nullable we can't say with certainty whether the test ought to fail"""
        a.node_attributes.is_nullable = True
        mock_structure = {
            a: [("b", self.violates_nullable)],
            b: [("c", self.violates_nullable)],
            c: [],
        }
        G = get_analysis_from_map(mock_structure)
        results = G.test_nullable_violations(name="a", namespace=DEFAULT_NAMESPACE, is_nullable=True)
        assert len(results) == 0

    # @get_nodes(n=3)
    # def test_violates_self_information(self, a, b, c):
    #     """If the initial node expect expects different nullableness it should be identified"""
    #     a.node_attributes.is_nullable = True
    #     mock_structure = {
    #         a: [("b", self.preserves_nullable)],
    #         b: [("c", self.preserves_nullable)],
    #         c: [],
    #     }
    #     G = get_analysis_from_map(mock_structure)
    #     results = G.test_nullable_violations(name="a", namespace=DEFAULT_NAMESPACE, is_nullable=False)
    #
    #     assert len(results) == 1 and results[0][-1].spec.name is "a", results

    @get_nodes(n=4)
    def test_nullable_skip_violation(self, a, b, c, d):
        """Test failures should be detected even multiple jumps from the source node"""
        d.node_attributes.is_nullable = False
        mock_structure = {
            a: [("b", self.preserves_nullable)],
            b: [("c", self.preserves_nullable)],
            c: [("d", self.preserves_nullable)],
            d: [],
        }
        G = get_analysis_from_map(mock_structure)
        results = G.test_nullable_violations(name="a", namespace=DEFAULT_NAMESPACE, is_nullable=True)
        assert (
            len(results) == 1 and results[0][0][-1].spec.name is "d"
        ), "Test failure not detected multiple steps from source node"

    @get_nodes(n=3)
    def test_triangle_violation(self, a, b, c):
        """Tests ought to be able to fail following multiple different paths through lineage"""
        c.node_attributes.is_nullable = False
        mock_structure = {
            a: [("b", self.preserves_nullable), ("c", self.preserves_nullable)],
            b: [("c", self.preserves_nullable)],
            c: [],
        }
        G = get_analysis_from_map(mock_structure)
        results = G.test_nullable_violations(name="a", namespace=DEFAULT_NAMESPACE, is_nullable=True)
        assert len(results) == 2 and results[0][0][-1].spec.name is "c" and results[1][0][-1].spec.name is "c"


class TestDataType(unittest.TestCase):
    preserves_data_type = ColumnToColumnAttributes(preserves_data_type=True)
    violates_data_type = ColumnToColumnAttributes(preserves_data_type=False)
    unknown_data_type = ColumnToColumnAttributes()

    def get_nodes(n: int = 3):
        variables = "abcdefghijklmnopqrstuvwxyz"
        extra_kwargs = {char: TestNodeObj(name=char, node_attributes={}) for char in variables[0:n]}

        def inner(fn):
            def wraps(*args, **kwargs):
                return fn(*args, **kwargs, **extra_kwargs)

            return wraps

        return inner

    @get_nodes(n=2)
    def test_table_to_column_information(self, a, b):
        """We don't know anything about node nullableness to evaluate failure or success"""
        mock_structure = {
            a: [("b", TableToColumnAttributes())],
            b: [],
        }
        G = get_analysis_from_map(mock_structure)
        results = G.test_data_type_change(name="a", namespace=DEFAULT_NAMESPACE, new_type="bool")
        assert len(results) == 0

    @get_nodes(n=2)
    def test_table_to_table_information(self, a, b):
        """We don't know anything about node nullableness to evaluate failure or success"""
        mock_structure = {
            a: [("b", TableToTableAttributes())],
            b: [],
        }
        G = get_analysis_from_map(mock_structure)
        results = G.test_data_type_change(name="a", namespace=DEFAULT_NAMESPACE, new_type="bool")
        assert len(results) == 0

    @get_nodes(n=3)
    def test_no_node_information(self, a, b, c):
        """We don't know anything about node nullableness to evaluate failure or success"""
        mock_structure = {
            a: [("b", self.preserves_data_type)],
            b: [("c", self.preserves_data_type)],
            c: [],
        }
        G = get_analysis_from_map(mock_structure)
        results = G.test_data_type_change(name="a", namespace=DEFAULT_NAMESPACE, new_type="bool")
        assert len(results) == 0

    @get_nodes(n=3)
    def test_no_node_or_edge_information(self, a, b, c):
        """We don't know anything about node nullableness to evaluate failure or success"""
        mock_structure = {
            a: [("b", self.preserves_data_type)],
            b: [("c", self.preserves_data_type)],
            c: [],
        }
        G = get_analysis_from_map(mock_structure)
        results = G.test_data_type_change(name="a", namespace=DEFAULT_NAMESPACE, new_type="bool")
        assert len(results) == 0

    @get_nodes(n=3)
    def test_violates_nullable(self, a, b, c):
        """If the edge doesn't preserve nullable we can't say with certainty whether the test ought to fail"""
        a.node_attributes.data_type = "bool"
        mock_structure = {
            a: [("b", self.violates_data_type)],
            b: [("c", self.violates_data_type)],
            c: [],
        }
        G = get_analysis_from_map(mock_structure)
        results = G.test_data_type_change(name="a", namespace=DEFAULT_NAMESPACE, new_type="bool")
        assert len(results) == 0

    # @get_nodes(n=3)
    # def test_violates_self_information(self, a, b, c):
    #     """If the initial node expect expects different nullableness it should be identified"""
    #     a.node_attributes.data_type = "bool"
    #     mock_structure = {
    #         a: [("b", self.preserves_data_type)],
    #         b: [("c", self.preserves_data_type)],
    #         c: [],
    #     }
    #     G = get_analysis_from_map(mock_structure)
    #     results = G.test_data_type_change(name="a", namespace=DEFAULT_NAMESPACE, new_type="int")
    #
    #     assert len(results) == 1 and results[0][0][-1].spec.name is "a", results

    @get_nodes(n=4)
    def test_skip_violation(self, a, b, c, d):
        """Test failures should be detected even multiple jumps from the source node"""
        d.node_attributes.data_type = "bool"
        mock_structure = {
            a: [("b", self.preserves_data_type)],
            b: [("c", self.preserves_data_type)],
            c: [("d", self.preserves_data_type)],
            d: [],
        }
        G = get_analysis_from_map(mock_structure)

        results = G.test_data_type_change(name="a", namespace=DEFAULT_NAMESPACE, new_type="int")
        assert (
            len(results) == 1 and results[0][0][-1].spec.name is "d"
        ), "Test failure not detected multiple steps from source node"

    @get_nodes(n=3)
    def test_triangle_violation(self, a, b, c):
        """Tests ought to be able to fail following multiple different paths through lineage"""
        c.node_attributes.data_type = "bool"
        mock_structure = {
            a: [("b", self.preserves_data_type), ("c", self.preserves_data_type)],
            b: [("c", self.preserves_data_type)],
            c: [],
        }
        G = get_analysis_from_map(mock_structure)
        results = G.test_data_type_change(name="a", namespace=DEFAULT_NAMESPACE, new_type="int")
        assert len(results) == 2 and results[0][0][-1].spec.name is "c" and results[1][0][-1].spec.name is "c"

import unittest
import uuid

import networkx as nx
import pytest
from grai_schemas.v1 import OrganisationV1, WorkspaceV1
from grai_schemas.v1.edge import EdgeV1, SourcedEdgeV1
from grai_schemas.v1.metadata.edges import (
    ColumnToColumnAttributes,
    TableToColumnAttributes,
    TableToTableAttributes,
)
from grai_schemas.v1.mock import MockV1
from grai_schemas.v1.node import NodeV1, SourcedNodeV1

from grai_graph import graph
from grai_graph.utils import (
    DEFAULT_NAMESPACE,
    TestNodeObj,
    build_graph_from_map,
    get_analysis_from_map,
)


def get_node_id(node):
    """

    Args:
        node:

    Returns:

    Raises:

    """
    return {"name": node.name, "namespace": node.namespace}


def test_v1_build_sourced_graph():
    """ """
    edges = []
    nodes = []
    for i in range(4):
        s_node = MockV1().node.named_source_node_spec()
        d_node = MockV1().node.named_source_node_spec()
        test_edge = MockV1().edge.named_source_edge_spec(
            source=s_node,
            destination=d_node,
        )
        edges.append(SourcedEdgeV1.from_spec(test_edge))
        nodes.extend(
            [
                SourcedNodeV1.from_spec({**node.dict(), "data_source": test_edge.data_source})
                for node in [s_node, d_node]
            ]
        )
    G = graph.build_graph(nodes, edges, "v1")
    assert isinstance(G.graph, nx.DiGraph)


def test_v1_build_graph():
    """ """
    edges = []
    nodes = []
    for i in range(4):
        source = MockV1().source.source_spec()
        s_node = MockV1().node.named_node_spec(id=uuid.uuid4(), data_sources=[source])
        d_node = MockV1().node.named_node_spec(id=uuid.uuid4(), data_sources=[source])
        test_edge = MockV1().edge.named_edge_spec(
            id=uuid.uuid4(), source=s_node, destination=d_node, data_sources=[source]
        )

        edges.append(EdgeV1.from_spec(test_edge))
        nodes.extend([NodeV1.from_spec(node) for node in [s_node, d_node]])
    G = graph.build_graph(nodes, edges, "v1")
    assert isinstance(G.graph, nx.DiGraph)


class TestUniqueness(unittest.TestCase):
    """ """

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
        """We don't know anything about node nullableness to evaluate failure or success

        Args:
            a:
            b:

        Returns:

        Raises:

        """
        mock_structure = {
            a: [("b", TableToColumnAttributes())],
            b: [],
        }
        G = get_analysis_from_map(mock_structure)
        results = G.test_unique_violations(name="a", namespace=DEFAULT_NAMESPACE, expects_unique=True)
        assert len(results) == 0

    @get_nodes(n=2)
    def test_table_to_table_information(self, a, b):
        """We don't know anything about node nullableness to evaluate failure or success

        Args:
            a:
            b:

        Returns:

        Raises:

        """
        mock_structure = {
            a: [("b", TableToTableAttributes())],
            b: [],
        }
        G = get_analysis_from_map(mock_structure)
        results = G.test_unique_violations(name="a", namespace=DEFAULT_NAMESPACE, expects_unique=True)
        assert len(results) == 0

    @get_nodes(n=3)
    def test_no_node_information(self, a, b, c):
        """We don't know anything about node uniqueness to evaluate failure or success

        Args:
            a:
            b:
            c:

        Returns:

        Raises:

        """
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
        """If the edge doesn't preserve unique we can't say with certainty whether the test ought to fail

        Args:
            a:
            b:
            c:

        Returns:

        Raises:

        """
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
        """Test failures should be detected even multiple jumps from the source node

        Args:
            a:
            b:
            c:
            d:

        Returns:

        Raises:

        """
        d.node_attributes.is_unique = False
        mock_structure = {
            a: [("b", self.preserves_unique)],
            b: [("c", self.preserves_unique)],
            c: [("d", self.preserves_unique)],
            d: [],
        }
        G = get_analysis_from_map(mock_structure)
        results = G.test_unique_violations(name="a", namespace=DEFAULT_NAMESPACE, expects_unique=True)
        assert len(results) == 1
        assert results[0][0][-1].spec.name == "d", results

    @get_nodes(n=3)
    def test_triangle_violation(self, a, b, c):
        """Tests ought to be able to fail following multiple different paths through lineage

        Args:
            a:
            b:
            c:

        Returns:

        Raises:

        """
        c.node_attributes.is_unique = False
        mock_structure = {
            a: [("b", self.preserves_unique), ("c", self.preserves_unique)],
            b: [("c", self.preserves_unique)],
            c: [],
        }
        G = get_analysis_from_map(mock_structure)
        results = G.test_unique_violations(name="a", namespace=DEFAULT_NAMESPACE, expects_unique=True)
        assert len(results) == 2 and results[0][0][-1].spec.name == "c" and results[1][0][-1].spec.name == "c"


class TestNullable(unittest.TestCase):
    """ """

    preserves_nullable = ColumnToColumnAttributes(preserves_nullable=True)
    violates_nullable = ColumnToColumnAttributes(preserves_nullable=False)
    unknown_nullable = ColumnToColumnAttributes()

    def get_nodes(n: int = 3):
        """

        Args:
            n (int, optional): (Default value = 3)

        Returns:

        Raises:

        """
        variables = "abcdefghijklmnopqrstuvwxyz"
        extra_kwargs = {char: TestNodeObj(name=char, node_attributes={}) for char in variables[0:n]}

        def inner(fn):
            """

            Args:
                fn:

            Returns:

            Raises:

            """

            def wraps(*args, **kwargs):
                """

                Args:
                    *args:
                    **kwargs:

                Returns:

                Raises:

                """
                return fn(*args, **kwargs, **extra_kwargs)

            return wraps

        return inner

    @get_nodes(n=2)
    def test_table_to_column_information(self, a, b):
        """We don't know anything about node nullableness to evaluate failure or success

        Args:
            a:
            b:

        Returns:

        Raises:

        """
        mock_structure = {
            a: [("b", TableToColumnAttributes())],
            b: [],
        }
        G = get_analysis_from_map(mock_structure)
        results = G.test_nullable_violations(name="a", namespace=DEFAULT_NAMESPACE, is_nullable=True)
        assert len(results) == 0

    @get_nodes(n=2)
    def test_table_to_table_information(self, a, b):
        """We don't know anything about node nullableness to evaluate failure or success

        Args:
            a:
            b:

        Returns:

        Raises:

        """
        mock_structure = {
            a: [("b", TableToTableAttributes())],
            b: [],
        }
        G = get_analysis_from_map(mock_structure)
        results = G.test_nullable_violations(name="a", namespace=DEFAULT_NAMESPACE, is_nullable=True)
        assert len(results) == 0

    @get_nodes(n=3)
    def test_no_node_information(self, a, b, c):
        """We don't know anything about node nullableness to evaluate failure or success

        Args:
            a:
            b:
            c:

        Returns:

        Raises:

        """
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
        """We don't know anything about node nullableness to evaluate failure or success

        Args:
            a:
            b:
            c:

        Returns:

        Raises:

        """
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
        """If the edge doesn't preserve nullable we can't say with certainty whether the test ought to fail

        Args:
            a:
            b:
            c:

        Returns:

        Raises:

        """
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
        """Test failures should be detected even multiple jumps from the source node

        Args:
            a:
            b:
            c:
            d:

        Returns:

        Raises:

        """
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
            len(results) == 1 and results[0][0][-1].spec.name == "d"
        ), "Test failure not detected multiple steps from source node"

    @get_nodes(n=3)
    def test_triangle_violation(self, a, b, c):
        """Tests ought to be able to fail following multiple different paths through lineage

        Args:
            a:
            b:
            c:

        Returns:

        Raises:

        """
        c.node_attributes.is_nullable = False
        mock_structure = {
            a: [("b", self.preserves_nullable), ("c", self.preserves_nullable)],
            b: [("c", self.preserves_nullable)],
            c: [],
        }
        G = get_analysis_from_map(mock_structure)
        results = G.test_nullable_violations(name="a", namespace=DEFAULT_NAMESPACE, is_nullable=True)
        assert len(results) == 2 and results[0][0][-1].spec.name == "c" and results[1][0][-1].spec.name == "c"


class TestDataType(unittest.TestCase):
    """ """

    preserves_data_type = ColumnToColumnAttributes(preserves_data_type=True)
    violates_data_type = ColumnToColumnAttributes(preserves_data_type=False)
    unknown_data_type = ColumnToColumnAttributes()

    def get_nodes(n: int = 3):
        """

        Args:
            n (int, optional): (Default value = 3)

        Returns:

        Raises:

        """
        variables = "abcdefghijklmnopqrstuvwxyz"
        extra_kwargs = {char: TestNodeObj(name=char, node_attributes={}) for char in variables[0:n]}

        def inner(fn):
            """

            Args:
                fn:

            Returns:

            Raises:

            """

            def wraps(*args, **kwargs):
                """

                Args:
                    *args:
                    **kwargs:

                Returns:

                Raises:

                """
                return fn(*args, **kwargs, **extra_kwargs)

            return wraps

        return inner

    @get_nodes(n=2)
    def test_table_to_column_information(self, a, b):
        """We don't know anything about node nullableness to evaluate failure or success

        Args:
            a:
            b:

        Returns:

        Raises:

        """
        mock_structure = {
            a: [("b", TableToColumnAttributes())],
            b: [],
        }
        G = get_analysis_from_map(mock_structure)
        results = G.test_data_type_change(name="a", namespace=DEFAULT_NAMESPACE, new_type="bool")
        assert len(results) == 0

    @get_nodes(n=2)
    def test_table_to_table_information(self, a, b):
        """We don't know anything about node nullableness to evaluate failure or success

        Args:
            a:
            b:

        Returns:

        Raises:

        """
        mock_structure = {
            a: [("b", TableToTableAttributes())],
            b: [],
        }
        G = get_analysis_from_map(mock_structure)
        results = G.test_data_type_change(name="a", namespace=DEFAULT_NAMESPACE, new_type="bool")
        assert len(results) == 0

    @get_nodes(n=3)
    def test_no_node_information(self, a, b, c):
        """We don't know anything about node nullableness to evaluate failure or success

        Args:
            a:
            b:
            c:

        Returns:

        Raises:

        """
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
        """We don't know anything about node nullableness to evaluate failure or success

        Args:
            a:
            b:
            c:

        Returns:

        Raises:

        """
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
        """If the edge doesn't preserve nullable we can't say with certainty whether the test ought to fail

        Args:
            a:
            b:
            c:

        Returns:

        Raises:

        """
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
        """Test failures should be detected even multiple jumps from the source node

        Args:
            a:
            b:
            c:
            d:

        Returns:

        Raises:

        """
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
            len(results) == 1 and results[0][0][-1].spec.name == "d"
        ), "Test failure not detected multiple steps from source node"

    @get_nodes(n=3)
    def test_triangle_violation(self, a, b, c):
        """Tests ought to be able to fail following multiple different paths through lineage

        Args:
            a:
            b:
            c:

        Returns:

        Raises:

        """
        c.node_attributes.data_type = "bool"
        mock_structure = {
            a: [("b", self.preserves_data_type), ("c", self.preserves_data_type)],
            b: [("c", self.preserves_data_type)],
            c: [],
        }
        G = get_analysis_from_map(mock_structure)
        results = G.test_data_type_change(name="a", namespace=DEFAULT_NAMESPACE, new_type="int")
        assert len(results) == 2 and results[0][0][-1].spec.name == "c" and results[1][0][-1].spec.name == "c"

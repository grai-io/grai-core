import pytest
from grai_source_dbt.base import get_nodes_and_edges
from grai_source_dbt.utils import get_manifest_file

from grai_graph import graph
from grai_graph.test_utils import TestNodeObj

TestNodeObj.__test__ = False


@pytest.fixture
def jaffle_shop_manifest():
    return get_manifest_file("jaffle_shop")


@pytest.fixture
def jaffle_nodes_and_edges(jaffle_shop_manifest):
    return get_nodes_and_edges(jaffle_shop_manifest)


@pytest.fixture
def jaffle_graph(jaffle_nodes_and_edges):
    nodes, edges = jaffle_nodes_and_edges
    jaffle_graph = graph.build_graph(nodes, edges, "v1")
    return jaffle_graph

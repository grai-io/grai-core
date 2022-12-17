import pytest
from grai_source_dbt.adapters import adapt_to_client
from grai_source_dbt.loader import DBTGraph, Manifest
from grai_source_dbt.models.tests import Test
from grai_source_dbt.utils import load_dbt_graph, load_from_manifest

Test.__test__ = False


@pytest.fixture
def dbt_graph() -> DBTGraph:
    return load_dbt_graph()


@pytest.fixture
def manifest() -> Manifest:
    return load_from_manifest()


@pytest.fixture
def v1_adapted_nodes(dbt_graph):
    return adapt_to_client(dbt_graph.nodes, "v1")


@pytest.fixture
def v1_adapted_edges(dbt_graph):
    return adapt_to_client(dbt_graph.edges, "v1")

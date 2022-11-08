import os
import pickle
from functools import cache

from grai_source_dbt.adapters import adapt_to_client
from grai_source_dbt.loader import DBTGraph, Manifest
from grai_source_dbt.test_utils import load_dbt_graph, load_from_manifest


def test_load_from_manifest():
    manifest = load_from_manifest()
    assert isinstance(manifest, Manifest)


# TODO: Validatation beyond runs without error
def test_get_all_nodes_and_edges():
    dbt_graph = load_dbt_graph()

    assert isinstance(dbt_graph, DBTGraph)
    assert len(dbt_graph.nodes) > 0
    assert len(dbt_graph.edges) > 0


# TODO: Validatation beyond runs without error
def test_v1_adapt_nodes():
    dbt_graph = load_dbt_graph()
    nodes = adapt_to_client(dbt_graph.nodes, "v1")


# TODO: Validatation beyond runs without error
def test_v1_adapt_edges():
    dbt_graph = load_dbt_graph()
    edges = adapt_to_client(dbt_graph.edges, "v1")

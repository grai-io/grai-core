import os
import pickle
from functools import cache

import pytest
from grai_client.schemas.edge import EdgeV1
from grai_client.schemas.node import NodeV1
from grai_source_dbt.adapters import adapt_to_client
from grai_source_dbt.loader import DBTGraph, Manifest
from grai_source_dbt.test_utils import load_dbt_graph, load_from_manifest


@pytest.fixture
def dbt_graph():
    return load_dbt_graph()


@pytest.fixture
def v1_adapted_nodes(dbt_graph):
    return adapt_to_client(dbt_graph.nodes, "v1")


@pytest.fixture
def v1_adapted_edges(dbt_graph):
    return adapt_to_client(dbt_graph.edges, "v1")


def test_load_from_manifest():
    manifest = load_from_manifest()
    assert isinstance(manifest, Manifest)


def test_build_dbt_graph(dbt_graph):
    assert isinstance(dbt_graph, DBTGraph)


def test_graph_nodes_created(dbt_graph):
    assert len(dbt_graph.nodes) > 0


def test_graph_edges_created(dbt_graph):
    assert len(dbt_graph.edges) > 0


def test_v1_adapt_nodes(v1_adapted_nodes):
    test_type = NodeV1
    for item in v1_adapted_nodes:
        assert isinstance(item, test_type), f"{item} is not of type {test_type}"


def test_v1_adapt_edges(v1_adapted_edges):
    test_type = EdgeV1
    for item in v1_adapted_edges:
        assert isinstance(item, test_type), f"{item} is not of type {test_type}"


def test_v1_adapted_edge_sources_have_nodes(v1_adapted_nodes, v1_adapted_edges):
    node_ids = {(n.spec.namespace, n.spec.name) for n in v1_adapted_nodes}
    edge_source_ids = {
        (n.spec.source.namespace, n.spec.source.name) for n in v1_adapted_edges
    }
    assert (
        len(edge_source_ids - node_ids) == 0
    ), "All edge sources should exist in the node list"


def test_v1_adapted_edge_destination_have_nodes(v1_adapted_nodes, v1_adapted_edges):
    node_ids = {(n.spec.namespace, n.spec.name) for n in v1_adapted_nodes}
    edge_destination_ids = {
        (n.spec.destination.namespace, n.spec.destination.name)
        for n in v1_adapted_edges
    }
    assert (
        len(edge_destination_ids - node_ids) == 0
    ), "All edge destinations should exist in the node list"

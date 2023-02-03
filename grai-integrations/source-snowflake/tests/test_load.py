from grai_schemas.v1 import EdgeV1, NodeV1


def test_v1_adapted_nodes_have_name(v1_adapted_nodes):
    assert all(node.spec.name is not None for node in v1_adapted_nodes)


def test_v1_adapted_nodes_have_namespace(v1_adapted_nodes):
    assert all(node.spec.namespace is not None for node in v1_adapted_nodes)


def test_v1_adapted_edge_source_has_name(v1_adapted_edges):
    assert all(edge.spec.source.name is not None for edge in v1_adapted_edges)


def test_v1_adapted_edge_source_has_namespace(v1_adapted_edges):
    assert all(edge.spec.source.namespace is not None for edge in v1_adapted_edges)


def test_v1_adapted_edge_destination_has_name(v1_adapted_edges):
    assert all(edge.spec.destination.name is not None for edge in v1_adapted_edges)


def test_v1_adapted_edge_destination_has_namespace(v1_adapted_edges):
    assert all(edge.spec.destination.namespace is not None for edge in v1_adapted_edges)


def test_v1_adapt_nodes(v1_adapted_nodes):
    test_type = NodeV1
    for item in v1_adapted_nodes:
        assert isinstance(item, test_type), f"{type(item)} is not of type {test_type}"


def test_v1_adapt_edges(v1_adapted_edges):
    test_type = EdgeV1
    for item in v1_adapted_edges:
        assert isinstance(item, test_type), f"{type(item)} is not of type {test_type}"


# Need to source these from a db for the tests to make sense.
# def test_v1_adapted_edge_sources_have_nodes(v1_adapted_nodes, v1_adapted_edges):
#     node_ids = {(n.spec.namespace, n.spec.name) for n in v1_adapted_nodes}
#     edge_source_ids = {(n.spec.source.namespace, n.spec.source.name) for n in v1_adapted_edges}
#     assert len(edge_source_ids - node_ids) == 0, f"All edge sources should exist in the node list {edge_source_ids - node_ids}"
#
#
# def test_v1_adapted_edge_destination_have_nodes(v1_adapted_nodes, v1_adapted_edges):
#     node_ids = {(n.spec.namespace, n.spec.name) for n in v1_adapted_nodes}
#     edge_destination_ids = {(n.spec.destination.namespace, n.spec.destination.name) for n in v1_adapted_edges}
#     assert len(edge_destination_ids - node_ids) == 0, "All edge destinations should exist in the node list"

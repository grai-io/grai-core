from grai_schemas.v1 import (
    EdgeV1,
    NodeV1,
    OrganisationV1,
    SourcedEdgeV1,
    SourcedNodeV1,
    WorkspaceV1,
)
from grai_schemas.v1.mock import MockV1

# `
# def test_mock_node_v1_validity():
#     mock = MockV1.node.node_dict()
#     node = NodeV1(**mock)
#     assert isinstance(node, NodeV1)
#     assert node.spec.metadata.sources
#
#
# def test_mock_sourced_node_v1_validity():
#     mock = MockV1.node.sourced_node_dict()
#     node = SourcedNodeV1(**mock)
#     breakpoint()
#     assert isinstance(node, SourcedNodeV1)
#
#
# def test_mock_edge_v1_validity():
#     mock = MockV1.edge.edge_dict()
#     edge = EdgeV1(**mock)
#     assert isinstance(edge, EdgeV1)
#
#
# def test_mock_sourced_edge_v1_validity():
#     mock = MockV1.edge.sourced_edge_dict()
#     edge = SourcedEdgeV1(**mock)
#     assert isinstance(edge, SourcedEdgeV1)
#
#
# def test_mock_workspace_v1_validity():
#     mock = MockV1.workspace.workspace_dict()
#     workspace = WorkspaceV1(**mock)
#     assert isinstance(workspace, WorkspaceV1)
#
#
# def test_mock_organisation_v1_validity():
#     mock = MockV1.organisation.organisation_dict()
#     organisation = OrganisationV1(**mock)
#     assert isinstance(organisation, OrganisationV1)

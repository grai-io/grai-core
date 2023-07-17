import pytest
from grai_schemas.v1 import (
    EdgeV1,
    NodeV1,
    OrganisationV1,
    SourcedEdgeV1,
    SourcedNodeV1,
    WorkspaceV1,
)
from grai_schemas.v1.mock import MockV1

mocks = [
    MockV1(),
    MockV1(workspace=MockV1().workspace.workspace()),
    MockV1(organisation=MockV1().organisation.organisation()),
    MockV1(workspace=MockV1().workspace.workspace(), organisation=MockV1().organisation.organisation()),
]

ids = ["no-defaults", "default-workspace", "default-organisation", "default-workspace-organisation"]


@pytest.mark.parametrize("mock", mocks, ids=ids)
class TestMockV1:
    def test_mock_node_v1(self, mock):
        assert isinstance(mock.node.node(), NodeV1)

    def test_mock_sourced_node_v1(self, mock):
        assert isinstance(mock.node.sourced_node(), SourcedNodeV1)

    def test_mock_edge_v1(self, mock):
        assert isinstance(mock.edge.edge(), EdgeV1)

    def test_mock_sourced_edge_v1(self, mock):
        assert isinstance(mock.edge.sourced_edge(), SourcedEdgeV1)

    def test_mock_workspace_v1(self, mock):
        assert isinstance(mock.workspace.workspace(), WorkspaceV1)

    def test_mock_organisation_v1_validity(self, mock):
        assert isinstance(mock.organisation.organisation(), OrganisationV1)

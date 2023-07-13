import datetime
import uuid

import pytest
from grai_schemas.base import Edge, Node
from grai_schemas.schema import Schema
from grai_schemas.v1 import EdgeV1, NodeV1, SourcedEdgeV1, SourcedNodeV1, WorkspaceV1
from grai_schemas.v1.mock import MockV1
from grai_schemas.v1.organization import OrganisationV1
from grai_schemas.v1.source import SourceV1
from pydantic import ValidationError


@pytest.mark.parametrize(
    "test_type,result",
    [
        (NodeV1, True),
        (Node, True),
        (EdgeV1, False),
        (Edge, False),
    ],
)
def test_v1_node_typing(test_type, result):
    """

    Args:
        test_type:
        result:

    Returns:

    Raises:

    """
    obj_dict = MockV1.node.node().dict()
    obj = Schema(entity=obj_dict)
    assert isinstance(obj.entity, test_type) == result, f"{type(obj)}=={test_type} should be {result}"


@pytest.mark.parametrize(
    "test_type,result",
    [
        (NodeV1, False),
        (Node, False),
        (EdgeV1, True),
        (Edge, True),
    ],
)
def test_v1_edge_typing(test_type, result):
    """

    Args:
        test_type:
        result:

    Returns:

    Raises:

    """
    obj_dict = MockV1.edge.edge().dict()
    obj = Schema(entity=obj_dict)
    assert isinstance(obj.entity, test_type) == result, f"{type(obj)}=={test_type} should be {result}"


class TestNodeV1:
    @staticmethod
    def test_node_from_spec_no_grai_metadata():
        """ """
        obj_dict = MockV1.node.node().dict()["spec"]
        obj_dict["metadata"].pop("grai")
        obj_dict["metadata"]["test_values"] = (1, 2, 3)
        obj = NodeV1.from_spec(obj_dict)
        assert isinstance(obj, NodeV1)
        assert hasattr(obj.spec, "metadata")
        assert hasattr(obj.spec.metadata, "grai")
        obj_dict["metadata"]["test_values"] = (1, 2, 3)

    @staticmethod
    def test_node_from_spec_no_metadata():
        """ """

        obj_dict = MockV1.node.node().dict()["spec"]
        obj_dict.pop("metadata")
        obj = NodeV1.from_spec(obj_dict)
        assert isinstance(obj, NodeV1)
        assert hasattr(obj.spec, "metadata")
        assert hasattr(obj.spec.metadata, "grai")

    @staticmethod
    def test_adding_new_field_to_node_metadata():
        """ """
        obj = MockV1.node.node()
        obj.spec.metadata.new_field = "new_value"
        assert obj.spec.metadata.new_field == "new_value"

    @staticmethod
    def test_node_from_spec_preserves_extra():
        obj_dict = MockV1.node.node().dict()["spec"]
        obj_dict["metadata"]["test_values"] = (1, 2, 3)
        obj = NodeV1.from_spec(obj_dict)
        assert hasattr(obj.spec.metadata, "test_values")
        assert obj.spec.metadata.test_values == (1, 2, 3)

    @staticmethod
    def test_node_source_vs_node_hash():
        node = MockV1.node.node()
        node_dict = node.spec.dict()
        node_dict.pop("data_sources")
        node_dict["data_source"] = MockV1.node.named_source_node_spec()
        node_dict["metadata"] = list(node_dict["metadata"]["sources"].values())[0]
        source_node = SourcedNodeV1.from_spec(node_dict)
        assert hash(node) == hash(source_node)


class TestEdgeV1:
    @staticmethod
    def test_edge_from_spec_no_grai_metadata():
        """ """
        obj_dict = MockV1.edge.edge().dict()["spec"]
        obj_dict["metadata"].pop("grai")
        obj = EdgeV1.from_spec(obj_dict)
        assert isinstance(obj, EdgeV1)
        assert hasattr(obj.spec, "metadata")
        assert hasattr(obj.spec.metadata, "grai")

    @staticmethod
    def test_edge_from_spec_no_metadata():
        """ """
        obj_dict = MockV1.edge.edge().dict()["spec"]
        obj_dict.pop("metadata")
        obj = EdgeV1.from_spec(obj_dict)
        assert isinstance(obj, EdgeV1)
        assert hasattr(obj.spec, "metadata")
        assert hasattr(obj.spec.metadata, "grai")

    @staticmethod
    def test_adding_new_field_to_edge_metadata():
        """ """
        obj = MockV1.edge.edge()
        obj.spec.metadata.new_field = "new_value"
        assert obj.spec.metadata.new_field == "new_value"

    @staticmethod
    def test_edge_from_spec_preserves_extra():
        obj_dict = MockV1.edge.edge().dict()["spec"]
        obj_dict["metadata"]["test_values"] = (1, 2, 3)
        obj = EdgeV1.from_spec(obj_dict)
        assert hasattr(obj.spec.metadata, "test_values")
        assert obj.spec.metadata.test_values == (1, 2, 3)

    @staticmethod
    def test_edge_source_vs_edge_hash():
        edge = MockV1.edge.edge()
        edge_dict = edge.spec.dict()
        edge_dict.pop("data_sources")
        edge_dict["data_source"] = MockV1.node.named_source_node_spec()
        edge_dict["metadata"] = list(edge_dict["metadata"]["sources"].values())[0]
        source_edge = SourcedEdgeV1.from_spec(edge_dict)
        assert hash(edge) == hash(source_edge)


class TestWorkspaceV1:
    @staticmethod
    def test_default_workspace_valid_ref():
        data = MockV1.workspace.workspace().dict()["spec"]
        ws = WorkspaceV1.from_spec(data)
        assert ws.spec.ref == f"{ws.spec.organisation.name}/{ws.spec.name}"

    @staticmethod
    def test_default_workspace_missing_ref():
        data = MockV1.workspace.workspace().dict()["spec"]
        data.pop("ref", None)
        ws = WorkspaceV1.from_spec(data)
        assert ws.spec.ref == f"{ws.spec.organisation.name}/{ws.spec.name}"

    @staticmethod
    @pytest.mark.xfail(raises=ValidationError)
    def test_default_workspace_invalid_ref():
        data = MockV1.workspace.workspace().dict()["spec"]
        data["ref"] = "a/invalid/ref"
        ws = WorkspaceV1.from_spec(data)

    @staticmethod
    @pytest.mark.xfail(raises=ValidationError)
    def test_default_workspace_bad_ref():
        data = MockV1.workspace.workspace().dict()["spec"]
        data["ref"] = "test"
        ws = WorkspaceV1.from_spec(data)

    @staticmethod
    @pytest.mark.xfail(raises=ValidationError)
    def test_default_workspace_bad_ref():
        data = MockV1.workspace.workspace().dict()["spec"]
        data["ref"] = "test/1/2"
        ws = WorkspaceV1.from_spec(data)


class TestOrganisationV1:
    @staticmethod
    @pytest.mark.xfail(raises=ValidationError)
    def test_organisation_valid_name():
        data = MockV1.organisation.organisation().dict()["spec"]
        data["name"] = ["test"]
        org = OrganisationV1.from_spec(data)

    @staticmethod
    @pytest.mark.xfail(raises=ValidationError)
    def test_organisation_missing_name():
        data = MockV1.organisation.organisation().dict()["spec"]
        data.pop("name")
        org = OrganisationV1.from_spec(data)

    @staticmethod
    def test_organisation_missing_id():
        data = MockV1.organisation.organisation().dict()["spec"]
        data.pop("id")
        org = OrganisationV1.from_spec(data)
        assert org.spec.id is None

    @staticmethod
    @pytest.mark.xfail(raises=ValidationError)
    def test_organisation_invalid_id():
        data = MockV1.organisation.organisation().dict()["spec"]
        data["id"] = "not_a_uuid"
        org = OrganisationV1.from_spec(data)


class TestSourceV1:
    @staticmethod
    def test_source_missing_id():
        data = MockV1.source.source().dict()["spec"]
        data.pop("id")
        source = SourceV1.from_spec(data)
        assert source.spec.id is None

    @staticmethod
    @pytest.mark.xfail(raises=ValidationError)
    def test_source_missing_name():
        data = MockV1.source.source().dict()["spec"]
        data.pop("name")
        source = SourceV1.from_spec(data)

    @staticmethod
    @pytest.mark.xfail(raises=ValidationError)
    def test_source_missing_workspace():
        data = MockV1.source.source().dict()["spec"]
        data.pop("workspace", None)
        source = SourceV1.from_spec(data)

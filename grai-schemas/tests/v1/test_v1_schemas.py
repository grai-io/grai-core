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


def extra_metadata():
    return {
        "test_dict": {"a": "b"},
        "test_list": [1, 2, 3],
        "test_tuple": (4, 5, 6),
        "test_date": datetime.date(2021, 3, 14),
    }


def make_v1_node():
    """ """
    node = {
        "type": "Node",
        "version": "v1",
        "spec": {
            "id": uuid.uuid4(),
            "name": "test",
            "namespace": "test-ns",
            "data_source": "tests",
            "display_name": "ouch",
            "is_active": True,
            "metadata": {
                "grai": {"node_type": "Generic", "node_attributes": {}, "tags": ["pii", "phi"]},
                **extra_metadata(),
            },
        },
    }
    return {**node}


def make_v1_edge():
    """ """
    edge = {
        "type": "Edge",
        "version": "v1",
        "spec": {
            "id": uuid.uuid4(),
            "name": "test",
            "namespace": "test2",
            "data_source": "tests",
            "source": {
                "namespace": "sou",
                "name": "rce",
            },
            "destination": {
                "namespace": "desti",
                "name": "nation",
            },
            "is_active": True,
            "metadata": {
                "grai": {"edge_type": "Generic", "edge_attributes": {}, "tags": ["pii", "phi"]},
                **extra_metadata(),
            },
        },
    }
    return {**edge}


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
    obj_dict = MockV1.node.node_dict()
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
    obj_dict = MockV1.edge.edge_dict()
    obj = Schema(entity=obj_dict)
    assert isinstance(obj.entity, test_type) == result, f"{type(obj)}=={test_type} should be {result}"


# test adding a new field to the metadata of a node
def test_adding_new_field_to_node_metadata():
    """ """
    obj = MockV1.node.node()
    obj.spec.metadata.new_field = "new_value"
    assert obj.spec.metadata.new_field == "new_value"


def test_adding_new_field_to_edge_metadata():
    """ """
    obj = MockV1.edge.edge()
    obj.spec.metadata.new_field = "new_value"
    assert obj.spec.metadata.new_field == "new_value"


def test_node_from_spec_no_metadata():
    """ """

    obj_dict = MockV1.node.node_dict()["spec"]
    obj_dict.pop("metadata")
    obj = NodeV1.from_spec(obj_dict)
    assert isinstance(obj, NodeV1)
    assert hasattr(obj.spec, "metadata")
    assert hasattr(obj.spec.metadata, "grai")


def test_edge_from_spec_no_metadata():
    """ """
    obj_dict = MockV1.edge.edge_dict()["spec"]
    obj_dict.pop("metadata")
    obj = EdgeV1.from_spec(obj_dict)
    assert isinstance(obj, EdgeV1)
    assert hasattr(obj.spec, "metadata")
    assert hasattr(obj.spec.metadata, "grai")


def test_edge_from_spec_no_grai_metadata():
    """ """
    obj_dict = MockV1.edge.edge_dict()["spec"]
    obj_dict["metadata"].pop("grai")
    obj = EdgeV1.from_spec(obj_dict)
    assert isinstance(obj, EdgeV1)
    assert hasattr(obj.spec, "metadata")
    assert hasattr(obj.spec.metadata, "grai")


def test_node_from_spec_no_grai_metadata():
    """ """
    obj_dict = MockV1.node.node_dict()["spec"]
    obj_dict["metadata"].pop("grai")
    obj_dict["metadata"]["test_values"] = (1, 2, 3)
    obj = NodeV1.from_spec(obj_dict)
    assert isinstance(obj, NodeV1)
    assert hasattr(obj.spec, "metadata")
    assert hasattr(obj.spec.metadata, "grai")
    obj_dict["metadata"]["test_values"] = (1, 2, 3)


def test_node_from_spec_preserves_extra():
    obj_dict = MockV1.node.node_dict()["spec"]
    obj_dict["metadata"]["test_values"] = (1, 2, 3)
    obj = NodeV1.from_spec(obj_dict)
    assert hasattr(obj.spec.metadata, "test_values")
    assert obj.spec.metadata.test_values == (1, 2, 3)


def test_edge_from_spec_preserves_extra():
    obj_dict = MockV1.edge.edge_dict()["spec"]
    obj_dict["metadata"]["test_values"] = (1, 2, 3)
    obj = EdgeV1.from_spec(obj_dict)
    assert hasattr(obj.spec.metadata, "test_values")
    assert obj.spec.metadata.test_values == (1, 2, 3)


def test_node_source_vs_node_hash():
    node = MockV1.node.node()
    node_dict = node.spec.dict()
    node_dict["data_source"] = node_dict.pop("data_sources")[0]
    source_node = SourcedNodeV1.from_spec(node_dict)
    assert hash(node) == hash(source_node)


def test_edge_source_vs_edge_hash():
    edge = MockV1.edge.edge()
    edge_dict = edge.spec.dict()
    edge_dict["data_source"] = edge_dict.pop("data_sources")[0]
    source_edge = SourcedEdgeV1.from_spec(edge_dict)
    assert hash(edge) == hash(source_edge)


class TestWorkspaceV1:
    @staticmethod
    def test_default_workspace_valid_ref():
        data = MockV1.workspace.workspace_dict()["spec"]
        ws = WorkspaceV1.from_spec(data)
        assert ws.spec.ref == f"{ws.spec.organisation.name}/{ws.spec.name}"

    @staticmethod
    def test_default_workspace_missing_ref():
        data = MockV1.workspace.workspace_dict()["spec"]
        data.pop("ref", None)
        ws = WorkspaceV1.from_spec(data)
        assert ws.spec.ref == f"{ws.spec.organisation.name}/{ws.spec.name}"

    @staticmethod
    @pytest.mark.xfail(raises=ValidationError)
    def test_default_workspace_invalid_ref():
        data = MockV1.workspace.workspace_dict()["spec"]
        data["ref"] = "a/invalid/ref"
        ws = WorkspaceV1.from_spec(data)

    @staticmethod
    @pytest.mark.xfail(raises=ValidationError)
    def test_default_workspace_bad_ref():
        data = MockV1.workspace.workspace_dict()["spec"]
        data["ref"] = "test"
        ws = WorkspaceV1.from_spec(data)

    @staticmethod
    @pytest.mark.xfail(raises=ValidationError)
    def test_default_workspace_bad_ref():
        data = MockV1.workspace.workspace_dict()["spec"]
        data["ref"] = "test/1/2"
        ws = WorkspaceV1.from_spec(data)


class TestOrganisationV1:
    @staticmethod
    @pytest.mark.xfail(raises=ValidationError)
    def test_organisation_valid_name():
        data = MockV1.organisation.organisation_dict()["spec"]
        data["name"] = ["test"]
        org = OrganisationV1.from_spec(data)

    @staticmethod
    @pytest.mark.xfail(raises=ValidationError)
    def test_organisation_missing_name():
        data = MockV1.organisation.organisation_dict()["spec"]
        data.pop("name")
        org = OrganisationV1.from_spec(data)

    @staticmethod
    def test_organisation_missing_id():
        data = MockV1.organisation.organisation_dict()["spec"]
        data.pop("id")
        org = OrganisationV1.from_spec(data)
        assert org.spec.id is None

    @staticmethod
    @pytest.mark.xfail(raises=ValidationError)
    def test_organisation_invalid_id():
        data = MockV1.organisation.organisation_dict()["spec"]
        data["id"] = "not_a_uuid"
        org = OrganisationV1.from_spec(data)


class TestSourceV1:
    @staticmethod
    def test_source_missing_id():
        data = MockV1.source.source_dict()["spec"]
        data.pop("id")
        source = SourceV1.from_spec(data)
        assert source.spec.id is None

    @staticmethod
    @pytest.mark.xfail(raises=ValidationError)
    def test_source_missing_name():
        data = MockV1.source.source_dict()["spec"]
        data.pop("name")
        source = SourceV1.from_spec(data)

    @staticmethod
    @pytest.mark.xfail(raises=ValidationError)
    def test_source_missing_workspace():
        data = MockV1.source.source_dict()["spec"]
        data.pop("workspace", None)
        source = SourceV1.from_spec(data)
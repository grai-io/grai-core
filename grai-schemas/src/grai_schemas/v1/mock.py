import datetime
import uuid

from grai_schemas.human_ids import get_human_id
from grai_schemas.v1.edge import EdgeV1, SourcedEdgeV1
from grai_schemas.v1.node import NodeV1, SourcedNodeV1
from grai_schemas.v1.organization import OrganisationSpec, OrganisationV1
from grai_schemas.v1.source import SourceV1
from grai_schemas.v1.workspace import WorkspaceSpec, WorkspaceV1


class MockNode:
    @classmethod
    def node_metadata_dict(cls):
        return {
            "grai": {"node_type": "Generic", "node_attributes": {}, "tags": ["pii", "phi"]},
            "test_dict": {"a": "b"},
            "test_list": [1, 2, 3],
            "test_tuple": (4, 5, 6),
            "test_date": datetime.date(2021, 3, 14),
        }

    @classmethod
    def base_node_spec_dict(cls, **kwargs):
        """ """
        return {
            "id": kwargs.get("id", None),
            "name": kwargs.get("name", get_human_id()),
            "namespace": kwargs.get("namespace", get_human_id()),
            "display_name": kwargs.get("display_name", get_human_id()),
            "is_active": kwargs.get("is_active", True),
            "metadata": kwargs.get("metadata", cls.node_metadata_dict()),
        }

    @classmethod
    def sourced_node_dict(cls, **kwargs):
        """ """
        result = {"type": "SourceNode", "version": "v1", "spec": cls.base_node_spec_dict(**kwargs)}
        result["spec"]["data_source"] = kwargs.get("data_source", MockSource.source_dict()["spec"])
        return result

    @classmethod
    def sourced_node(cls, **kwargs):
        """ """
        return SourcedNodeV1(**cls.sourced_node_dict(**kwargs))

    @classmethod
    def node_dict(cls, **kwargs):
        """ """
        result = {"type": "Node", "version": "v1", "spec": cls.base_node_spec_dict(**kwargs)}
        result["spec"]["data_sources"] = kwargs.get("data_sources", [MockSource.source_dict()["spec"]])
        return result

    @classmethod
    def node(cls, **kwargs):
        """ """
        return NodeV1(**cls.node_dict(**kwargs))


class MockEdge:
    node_kwargs = ["data_sources"]

    @classmethod
    def edge_metadata_dict(cls):
        return {
            "grai": {"edge_type": "Generic", "edge_attributes": {}, "tags": ["pii", "phi"]},
        }

    @classmethod
    def base_edge_spec_dict(cls, **kwargs):
        """ """
        node_kwargs = {k: kwargs[k].copy() for k in cls.node_kwargs if k in kwargs}
        return {
            "id": kwargs.get("id", None),
            "name": kwargs.get("name", get_human_id()),
            "namespace": kwargs.get("namespace", get_human_id()),
            "source": kwargs.get("source", MockNode.node(**node_kwargs).spec),
            "destination": kwargs.get("destination", MockNode.node(**node_kwargs).spec),
            "is_active": kwargs.get("is_active", True),
            "metadata": kwargs.get("metadata", cls.edge_metadata_dict()),
        }

    @classmethod
    def sourced_edge_dict(cls, **kwargs):
        """ """
        result = {
            "type": "SourceEdge",
            "version": "v1",
            "spec": cls.base_edge_spec_dict(**kwargs),
        }
        result["spec"]["data_source"] = kwargs.get("data_source", MockSource.source_dict()["spec"])
        return result

    @classmethod
    def sourced_edge(cls, **kwargs):
        """ """
        if "data_source" in kwargs:
            kwargs["data_sources"] = [kwargs["data_source"]]
        return SourcedEdgeV1(**cls.sourced_edge_dict(**kwargs))

    @classmethod
    def edge_dict(cls, **kwargs):
        """ """

        result = {
            "type": "Edge",
            "version": "v1",
            "spec": cls.base_edge_spec_dict(**kwargs),
        }
        result["spec"]["data_sources"] = kwargs.get("data_sources", [MockSource.source_dict()["spec"]]).copy()
        return result

    @classmethod
    def edge(cls, **kwargs):
        """ """
        return EdgeV1(**cls.edge_dict(**kwargs))

    @classmethod
    def edge_and_nodes(cls, **kwargs):
        edge = cls.edge(**kwargs)
        source, destination = edge.spec.source, edge.spec.destination
        return edge, [source, destination]


class MockOrganisation:
    @classmethod
    def organisation_spec_dict(cls, **kwargs):
        return {
            "name": kwargs.get("name", get_human_id()),
            "id": kwargs.get("id", uuid.uuid4()),
        }

    @classmethod
    def organisation_dict(cls, **kwargs):
        """"""
        return {
            "type": "Organisation",
            "version": "v1",
            "spec": cls.organisation_spec_dict(**kwargs),
        }

    @classmethod
    def organisation(cls, **kwargs):
        """"""
        return OrganisationV1(**cls.organisation_dict(**kwargs))


class MockWorkspace:
    @classmethod
    def workspace_spec_dict(cls, **kwargs):
        result = {
            "id": kwargs.get("id", None),
            "name": kwargs.get("name", get_human_id()),
            "search_enabled": kwargs.get("search_enabled", True),
        }
        if "organisation" in kwargs:
            result["organisation"] = kwargs["organisation"]
        elif "organization" in kwargs:
            result["organisation"] = kwargs["organization"]
        else:
            result["organisation"] = MockOrganisation.organisation_spec_dict()
        return result

    @classmethod
    def workspace_spec(cls, **kwargs):
        return WorkspaceSpec(**cls.workspace_spec_dict(**kwargs))

    @classmethod
    def workspace_dict(cls, **kwargs):
        result = {"type": "Workspace", "version": "v1", "spec": cls.workspace_spec_dict(**kwargs)}

        if "ref" in kwargs:
            result["spec"]["ref"] = kwargs["ref"]
        # elif isinstance(kwargs.get("organisation"), dict):
        #     result["spec"]["ref"] = f"{result['spec']['organisation']['name']}/{result['spec']['name']}"
        elif not isinstance(result["spec"].get("organisation", None), (OrganisationSpec, dict)):
            message = (
                "In order to generate a workspace ref you must pass an organisation dict or manually specify the ref"
            )
            raise ValueError(message)

        return result

    @classmethod
    def workspace(cls, **kwargs):
        return WorkspaceV1(**cls.workspace_dict(**kwargs))


class MockSource:
    @classmethod
    def source_dict(cls, **kwargs):
        result = {
            "type": "Source",
            "version": "v1",
            "spec": {
                "id": kwargs.get("id", None),
                "name": kwargs.get("name", get_human_id()),
                # "workspace": kwargs.get("workspace", MockWorkspace.workspace_spec_dict()),
            },
        }
        return result

    @classmethod
    def source(cls, **kwargs):
        return SourceV1(**cls.source_dict(**kwargs))


class MockV1:
    node = MockNode
    edge = MockEdge
    organisation = MockOrganisation
    workspace = MockWorkspace
    source = MockSource

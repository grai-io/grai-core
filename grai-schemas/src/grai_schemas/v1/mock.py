import datetime
import uuid

from grai_schemas.human_ids import get_human_id


class MockV1:
    default_source = {
        "namespace": "sou",
        "name": "rce",
    }
    default_destination = {
        "namespace": "desti",
        "name": "nation",
    }

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
    def edge_metadata_dict(cls):
        return {
            "grai": {"edge_type": "Generic", "edge_attributes": {}, "tags": ["pii", "phi"]},
        }

    @classmethod
    def base_node_spec_dict(cls, **kwargs):
        """ """
        return {
            "id": kwargs.get("id", uuid.uuid4()),
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
        result["spec"]["data_source"] = kwargs.get("data_source", get_human_id())
        return result

    @classmethod
    def node_dict(cls, **kwargs):
        """ """
        result = {"type": "Node", "version": "v1", "spec": cls.base_node_spec_dict(**kwargs)}
        result["spec"]["data_sources"] = kwargs.get("data_sources", [get_human_id()])
        return result

    @classmethod
    def base_edge_spec_dict(cls, **kwargs):
        """ """
        return {
            "id": kwargs.get("id", uuid.uuid4()),
            "name": kwargs.get("name", get_human_id()),
            "namespace": kwargs.get("namespace", get_human_id()),
            "source": kwargs.get("source", cls.default_source),
            "destination": kwargs.get("destination", cls.default_destination),
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
        result["spec"]["data_source"] = kwargs.get("data_source", get_human_id())
        return result

    @classmethod
    def edge_dict(cls, **kwargs):
        """ """

        result = {
            "type": "Edge",
            "version": "v1",
            "spec": cls.base_edge_spec_dict(**kwargs),
        }
        result["spec"]["data_sources"] = kwargs.get("data_sources", [get_human_id()])
        return result

    @classmethod
    def organisation_dict(cls, id=None, name=None):
        """"""
        return {
            "type": "Organisation",
            "version": "v1",
            "spec": {
                "id": uuid.uuid4() if id is None else id,
                "name": get_human_id() if name is None else name,
            },
        }

    @classmethod
    def workspace_dict(cls, **kwargs):
        result = {
            "type": "Workspace",
            "version": "v1",
            "spec": {
                "id": kwargs.get("id", uuid.uuid4()),
                "name": kwargs.get("name", get_human_id()),
                "organization": kwargs.get("organization", get_human_id()),
                "search_enabled": kwargs.get("search_enabled", True),
            },
        }
        result["spec"]["ref"] = kwargs.get("ref", f"{result['spec']['organization']}/{result['spec']['name']}")
        return result

import datetime
import uuid

from grai_schemas.human_ids import get_human_id


class MockV1:
    @staticmethod
    def node_dict(
        id=None, name=None, namespace=None, data_source=None, metadata=None, display_name=None, is_active=True
    ):
        """ """
        return {
            "type": "Node",
            "version": "v1",
            "spec": {
                "id": uuid.uuid4() if id is None else id,
                "name": get_human_id() if name is None else name,
                "namespace": get_human_id() if namespace is None else name,
                "data_source": get_human_id() if data_source is None else data_source,
                "display_name": get_human_id() if display_name is None else display_name,
                "is_active": is_active,
                "metadata": {
                    "grai": {"node_type": "Node", "node_attributes": {}, "tags": ["pii", "phi"]},
                    "test_dict": {"a": "b"},
                    "test_list": [1, 2, 3],
                    "test_tuple": (4, 5, 6),
                    "test_date": datetime.date(2021, 3, 14),
                },
            },
        }

    def edge_dict(id=None, name=None, namespace=None, data_source=None):
        """ """
        return {
            "type": "Edge",
            "version": "v1",
            "spec": {
                "id": uuid.uuid4(),
                "name": get_human_id() if name is None else name,
                "namespace": get_human_id() if namespace is None else name,
                "data_source": get_human_id() if data_source is None else data_source,
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
                    "grai": {"edge_type": "Edge", "edge_attributes": {}, "tags": ["pii", "phi"]},
                },
            },
        }

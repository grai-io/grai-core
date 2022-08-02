from grai_client.schemas.node import NodeV1
from grai_client.schemas.edge import EdgeV1
from grai_client.schemas.schema import Schema
import uuid


def mock_v1_node(name=None, namespace=None, data_source=None, display_name=None, is_active=True, metadata={}):
    node_dict = {
        "type": "Node",
        "version": "v1",
        "spec": {
            "id": None,
            "name": str(uuid.uuid4()) if name is None else name,
            "namespace": 'client_mocking' if namespace is None else namespace,
            "data_source": str(uuid.uuid4()) if data_source is None else data_source,
            "display_name": str(uuid.uuid4()) if display_name is None else display_name,
            "is_active": is_active,
            "metadata": metadata,
        },
    }
    return NodeV1(**node_dict)

def mock_node_id():
    return {
        'name': str(uuid.uuid4()),
        'namespace': str(uuid.uuid4())
    }

def mock_v1_edge(name=None, namespace=None, data_source=None, source=None, destination=None, is_active=True, metadata={}):
    edge_dict = {
        "type": "Edge",
        "version": "v1",
        "spec": {
            "id": None,
            "name": str(uuid.uuid4()) if name is None else name,
            "namespace": str(uuid.uuid4()) if name is None else name,
            "data_source": str(uuid.uuid4()) if data_source is None else data_source,
            "source": mock_node_id() if source is None else source,
            "destination": mock_node_id() if destination is None else destination,
            "is_active": is_active,
            "metadata": metadata,
        },
    }
    return EdgeV1(**edge_dict)


def mock_v1_edge_and_nodes(name=None, data_source=None, is_active=True, metadata={}, namespace=None):
    node1 = mock_v1_node(namespace=namespace, data_source=data_source)
    node2 = mock_v1_node(namespace=namespace, data_source=data_source)

    edge_dict = {
        "type": "Edge",
        "version": "v1",
        "spec": {
            "id": None,
            "name": str(uuid.uuid4()) if name is None else name,
            "namespace": str(uuid.uuid4()) if name is None else name,
            "data_source": str(uuid.uuid4()) if data_source is None else data_source,
            "source": {k: getattr(node1.spec, k) for k in ['name', 'namespace']},
            "destination": {k: getattr(node2.spec, k) for k in ['name', 'namespace']},
            "is_active": is_active,
            "metadata": metadata,
        },
    }
    return EdgeV1(**edge_dict), [node1, node2]

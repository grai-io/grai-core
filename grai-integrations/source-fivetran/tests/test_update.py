import json

import dotenv
from grai_client.endpoints.v1.client import ClientV1

from grai_source_fivetran.base import get_nodes_and_edges, update_server
from grai_source_fivetran.loader import FivetranConnector

# def test_load_from_remote():
#     dotenv.load_dotenv()
#     # client = ClientV1("localhost", "8000", username="null@grai.io", password="super_secret")
#     kwargs = {"default_namespace": 'default_namespace'}
#     # breakpoint()
#     connector = FivetranConnector(**kwargs)
#     nodes, edges = get_nodes_and_edges(connector, 'v1')


# def test_loader_with_json_namespaces():
#     dotenv.load_dotenv()
#     namespaces = '{"happy": "monkey"}'
#     conn = FivetranConnector(namespaces=namespaces)
#     assert conn.namespace_map.keys() == {"happy"}
#     assert conn.namespace_map['happy'].source == "monkey"
#     assert conn.namespace_map['happy'].destination == "monkey"
#
#
# def test_loader_with_dict_namespaces():
#     dotenv.load_dotenv()
#     namespaces = {"happy": "monkey"}
#     conn = FivetranConnector(namespaces=namespaces)
#     assert conn.namespace_map.keys() == {"happy"}
#     assert conn.namespace_map['happy'].source == "monkey"
#     assert conn.namespace_map['happy'].destination == "monkey"


# def test_load_from_remote():
#     dotenv.load_dotenv()
#     client = ClientV1("localhost", "8000", username="null@grai.io", password="super_secret", insecure=True)
#     kwargs = {"default_namespace": "default_namespace"}
#     update_server(client, **kwargs)

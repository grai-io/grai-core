import uuid
import networkx as nx
from grai_graph import graph
from grai_client.testing.schema import mock_v1_node, mock_v1_edge
from grai_client.endpoints.v1.client import ClientV1


# TODO: This needs to be mocked
client_configs = {
    'host': 'localhost',
    'port': '8000'
}
auth = {'username': 'null@grai.io', 'password': 'super_secret'}


def test_v1_client_monkeypatch():
    client = ClientV1(**client_configs)
    client.set_authentication_headers(**auth)
    G = client.build_graph()
    assert isinstance(G, nx.DiGraph)

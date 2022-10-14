import uuid

import networkx as nx
from grai_client.endpoints.v1.client import ClientV1
from grai_client.testing.schema import mock_v1_edge, mock_v1_node

from grai_graph import graph

# TODO: This needs to be mocked
client_configs = {"host": "localhost", "port": "8000"}
auth = {"username": "null@grai.io", "password": "super_secret"}


def test_v1_client_monkeypatch():
    client = ClientV1(**client_configs)
    client.set_authentication_headers(**auth)
    G = client.build_graph()
    assert isinstance(G.graph, nx.DiGraph)

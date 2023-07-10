import dotenv

from grai_source_fivetran.base import FivetranIntegration

# def test_load_from_remote():
#     dotenv.load_dotenv()
#     # client = ClientV1("localhost", "8000", username="null@grai.io", password="super_secret")
#     kwargs = {"default_namespace": "default_namespace"}
#     # breakpoint()
#     conn = FivetranIntegration(**kwargs)
#     nodes, edges = conn.get_nodes_and_edges()


def test_loader_with_json_namespaces(mock_source):
    dotenv.load_dotenv()
    namespaces = '{"happy": "monkey"}'
    conn = FivetranIntegration(namespaces=namespaces, source=mock_source)
    assert conn.connector.namespace_map.keys() == {"happy"}
    assert conn.connector.namespace_map["happy"].source == "monkey"
    assert conn.connector.namespace_map["happy"].destination == "monkey"


def test_loader_with_dict_namespaces(mock_source):
    dotenv.load_dotenv()
    namespaces = {"happy": "monkey"}
    conn = FivetranIntegration(namespaces=namespaces, source=mock_source)
    assert conn.connector.namespace_map.keys() == {"happy"}
    assert conn.connector.namespace_map["happy"].source == "monkey"
    assert conn.connector.namespace_map["happy"].destination == "monkey"


def test_load_from_remote_and_update(client, mock_source, namespace_map):
    dotenv.load_dotenv()
    conn = FivetranIntegration.from_client(client, source=mock_source.name, namespaces=namespace_map)
    conn.update()

import dotenv

from grai_source_looker.base import LookerIntegrationk

# def test_loader_with_json_namespaces(mock_source):
#     dotenv.load_dotenv()
#     namespaces = '{"happy": "monkey"}'
#     conn = FivetranIntegration(namespaces=namespaces, source=mock_source)
#     assert "happy" in conn.connector.namespace_map
#     assert conn.connector.namespace_map["happy"].source == "monkey"
#     assert conn.connector.namespace_map["happy"].destination == "monkey"


# def test_loader_with_dict_namespaces(mock_source, namespace_map):
#     dotenv.load_dotenv()
#     namespaces = {"happy": "monkey"}
#     conn = FivetranIntegration(namespaces=namespaces, source=mock_source)
#     assert "happy" in conn.connector.namespace_map
#     assert conn.connector.namespace_map["happy"].source == "monkey"
#     assert conn.connector.namespace_map["happy"].destination == "monkey"


# def test_load_from_remote(mock_source):
#     dotenv.load_dotenv()
#     conn = FivetranIntegration(source=mock_source)
#     nodes, edges = conn.get_nodes_and_edges()


# def test_load_from_remote_and_update(client, mock_source, namespace_map, run_live):
#     dotenv.load_dotenv()
#     conn = FivetranIntegration.from_client(client, source=mock_source.name, namespaces=namespace_map)
#     if run_live:
#         conn.update()

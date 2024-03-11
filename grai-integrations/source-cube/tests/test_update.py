from grai_source_cube.base import CubeIntegration


def test_loader_with_json_namespaces(mock_source, local_config):
    namespaces = '{"happy": "monkey"}'
    conn = CubeIntegration(namespace_map=namespaces, source=mock_source, namespace="test", config=local_config)
    assert "happy" in conn.connector.namespace_map
    assert conn.connector.namespace_map["happy"] == "monkey"


def test_loader_with_dict_namespaces(mock_source, local_config):
    namespaces = {"happy": "monkey"}
    conn = CubeIntegration(namespace_map=namespaces, source=mock_source, namespace="test", config=local_config)
    assert "happy" in conn.connector.namespace_map
    assert conn.connector.namespace_map["happy"] == "monkey"

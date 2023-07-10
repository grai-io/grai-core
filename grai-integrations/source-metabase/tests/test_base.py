from grai_source_metabase.base import get_nodes_and_edges, update_server


def test_get_nodes_and_edges(connector):
    nodes, edges = get_nodes_and_edges(connector, "v1")
    assert len(nodes) > 0
    assert len(edges) > 0


def test_update_server(connector, client, has_client):
    if not has_client:
        return
    kwargs = {
        "namespaces": None,
        "metabase_namespace": "a_default_namespace",
        "username": "admin@metabase.local",
        "password": "Metapass123",
        "endpoint": "http://localhost:3001",
    }

    update_server(client, **kwargs)

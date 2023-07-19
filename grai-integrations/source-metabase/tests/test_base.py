from grai_source_metabase.base import MetabaseIntegration


def test_get_nodes_and_edges(integration):
    nodes, edges = integration.get_nodes_and_edges()
    assert len(nodes) > 0
    assert len(edges) > 0


def test_update_server(client, has_client, mock_source):
    if not has_client:
        return

    kwargs = {
        "namespaces": None,
        "metabase_namespace": "a_default_namespace",
        "username": "admin@metabase.local",
        "password": "Metapass123",
        "endpoint": "http://localhost:3001",
    }
    integration = MetabaseIntegration.from_client(client=client, source=mock_source, **kwargs)

    integration.update(client, **kwargs)

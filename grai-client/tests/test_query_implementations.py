from functools import cache

import pytest
from grai_schemas.v1 import EdgeV1, NodeV1
from requests import RequestException

from grai_client.endpoints.utilities import is_valid_uuid
from grai_client.testing.schema import mock_v1_edge_and_nodes, mock_v1_node


class TestNodeQueries:
    def test_node_id_request(self, client, node_v1):
        result = client.get("node", node_v1.spec.id)
        assert result.spec.id == node_v1.spec.id

    def test_node_name_query(self, client, node_v1):
        result = client.get("node", name=node_v1.spec.name)
        assert result[0].spec.name == node_v1.spec.name

    def test_node_namespace_query(self, client, node_v1):
        result = client.get("node", namespace=node_v1.spec.namespace)
        assert result[0].spec.namespace == node_v1.spec.namespace

    # test querying with is_active=True
    def test_node_is_active_query(self, client, node_v1):
        result = client.get("node", name=node_v1.spec.name, is_active=True)
        assert result[0].spec.is_active is True

    # test querying with is_active=False
    def test_node_is_not_active_query(self, client, node_v1):
        result = client.get("node", name=node_v1.spec.name, is_active=False)
        assert len(result) == 0

    # test querying for all nodes with the metadata grai node_type field of "Table"
    def test_node_type_query(self, client, node_v1):
        result = client.get("node", metadata__grai__node_type="Table")
        assert all(node.spec.metadata.grai.node_type == "Table" for node in result)

    # test querying for all nodes with created at dates before january 1 2019
    def test_node_created_at_query(self, client, node_v1):
        result = client.get("node", created_at__lt="2019-01-01")
        assert len(result) == 0


class TestEdgeQueries:
    # test querying for edges by namespace
    def test_edge_namespace_query(self, client, edge_v1):
        result = client.get("edge", namespace=edge_v1.spec.namespace)
        assert result[0].spec.namespace == edge_v1.spec.namespace

    # test querying for edges by name
    def test_edge_name_query(self, client, edge_v1):
        result = client.get("edge", name=edge_v1.spec.name)
        assert result[0].spec.name == edge_v1.spec.name

    # test querying for edges by id
    def test_edge_id_query(self, client, edge_v1):
        result = client.get("edge", edge_v1.spec.id)
        assert result.spec.id == edge_v1.spec.id

    # test querying for edges by source node id
    def test_edge_source_node_id_query(self, client, edge_v1):
        result = client.get("edge", source=edge_v1.spec.source.id)
        assert all(r.spec.source.id == edge_v1.spec.source.id for r in result)

    # test querying for edges by destination node id
    def test_edge_destination_node_id_query(self, client, edge_v1):
        result = client.get("edge", destination=edge_v1.spec.destination.id)
        assert all(r.spec.destination.id == edge_v1.spec.destination.id for r in result)

    # test querying with is_active=True
    def test_edge_is_active_query(self, client, edge_v1):
        result = client.get("edge", name=edge_v1.spec.name, is_active=True)
        assert result[0].spec.is_active is True

    # test querying with is_active=False
    def test_edge_is_not_active_query(self, client, edge_v1):
        result = client.get("edge", name=edge_v1.spec.name, is_active=False)
        assert len(result) == 0

    # test querying for all edges with the metadata grai edge_type field of "TableToColumn"
    def test_edge_type_query(self, client, edge_v1):
        result = client.get("edge", metadata__grai__edge_type="TableToColumn")
        assert all(edge.spec.metadata.grai.edge_type == "TableToColumn" for edge in result)

    # test querying for all edges with created at dates before january 1 2019
    def test_edge_created_at_query(self, client, edge_v1):
        result = client.get("edge", created_at__lt="2019-01-01")
        assert len(result) == 0

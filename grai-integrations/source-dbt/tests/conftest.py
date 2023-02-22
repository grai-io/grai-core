import pytest
from grai_client.endpoints.v1.client import ClientV1

# #from grai_source_dbt.adapters import adapt_to_client
# from grai_source_dbt.loader import Manifest
# from grai_source_dbt.models.tests import Test
# from grai_source_dbt.utils import load_from_manifest
#
# Test.__test__ = False
#

# @pytest.fixture
# def client() -> ClientV1:
#     test_credentials = {
#         "host": "localhost",
#         "port": "5432",
#         "dbname": "grai",
#         "user": "grai",
#         "password": "grai",
#         "namespace": "test",
#     }
#
#     client = ClientV1("localhost", "8000", workspace="default")
#     client.set_authentication_headers("null@grai.io", "super_secret")
#     return client


# @pytest.fixture
# def dbt_graph() -> DBTGraph:
#     return load_dbt_graph()
#
#
# @pytest.fixture
# def loader() -> Manifest:
#     return load_from_manifest()


# @pytest.fixture
# def v1_adapted_nodes(dbt_graph):
#     return adapt_to_client(dbt_graph.nodes, "v1")
#
#
# @pytest.fixture
# def v1_adapted_edges(dbt_graph):
#     return adapt_to_client(dbt_graph.edges, "v1")

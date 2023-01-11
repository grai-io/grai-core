# from grai_client.endpoints.v1.client import ClientV1
#
# from grai_source_dbt.base import update_server
# from grai_source_dbt.utils import get_manifest_file
#
# test_credentials = {
#     "host": "localhost",
#     "port": "5432",
#     "dbname": "grai",
#     "user": "grai",
#     "password": "grai",
#     "namespace": "test",
# }
#
#
# client = ClientV1("localhost", "8000", workspace="default")
# client.set_authentication_headers("null@grai.io", "super_secret")
#
#
# def test_update_server():
#     update_server(client, get_manifest_file())

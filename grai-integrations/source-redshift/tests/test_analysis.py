# from grai_client.endpoints.v1.client import ClientV1
#
# from grai_source_redshift.base import update_server
# from grai_source_redshift.loader import RedshiftConnector
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
# client = ClientV1("localhost", "8000", workspace="default", insecure=True)
# client.authenticate(username="null@grai.io", password="super_secret")
#
#
# def test_update():
#     update_server(client, namespace="default")

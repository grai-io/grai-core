# from grai_client.endpoints.v1.client import ClientV1
# from grai_source_mysql.base import update_server
# from grai_source_mysql.loader import MySQLConnector
#
# test_credentials = {
#     "host": "localhost",
#     "port": "3306",
#     "dbname": "grai",
#     "user": "grai",
#     "password": "grai",
#     "namespace": "test",
# }
#
#
# client = ClientV1("localhost", "8000")
# client.set_authentication_headers("null@grai.io", "super_secret")
#
#
# def test_update():
#     update_server(client, **test_credentials)

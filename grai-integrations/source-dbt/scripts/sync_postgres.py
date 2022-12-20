from grai_client.endpoints.v1.client import ClientV1
from grai_source_postgres.base import update_server

client = ClientV1("localhost", "8000")
client.set_authentication_headers(username="null@grai.io", password="super_secret")


update_server(
    client,
    host="localhost",
    port="5433",
    dbname="docker",
    user="docker",
    password="docker",
    namespace="default",
)

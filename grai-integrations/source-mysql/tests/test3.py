from grai_source_postgres.base import update_server
from grai_client.endpoints.v1.client import ClientV1

client = ClientV1("localhost","8000")
client.set_authentication_headers("null@grai.io","super_secret")

update_server(client, dbname='docker', user='docker', password='docker', namespace='jaffle_shop', host='localhost', port='5433')
from grai_client.endpoints.v1.client import ClientV1

from grai_source_dbt.base import get_nodes_and_edges, update, update_server
from grai_source_dbt.data_tools import get_manifest_file

client = ClientV1("localhost", "8000")
client.set_authentication_headers("null@grai.io", "super_secret")


update_server(client, get_manifest_file(), namespace="default")

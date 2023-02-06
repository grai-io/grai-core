import dotenv
from grai_client.endpoints.v1.client import ClientV1

from grai_source_snowflake.base import get_nodes_and_edges, update_server
from grai_source_snowflake.loader import SnowflakeConnector

dotenv.load_dotenv()


def test_update_server():
    client = ClientV1(host="localhost", port="8000")
    client.set_authentication_headers(username="null@grai.io", password="super_secret")
    update_server(client)
    # connector = SnowflakeConnector()
    # with connector as conn:
    #     breakpoint()


test_update_server()

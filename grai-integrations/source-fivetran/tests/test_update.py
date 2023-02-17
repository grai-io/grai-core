# from grai_source_fivetran.base import get_nodes_and_edges
# from grai_source_fivetran.loader import FivetranConnector
# import dotenv
#
#
# def test_load_from_remote():
#     dotenv.load_dotenv()
#     client = ClientV1("localhost", "8000")
#     client.set_authentication_headers("null@grai.io", "super_secret")
#     kwargs = {"default_namespace": 'default_namespace'}
#     connector = FivetranConnector(**kwargs)
#     nodes, edges = get_nodes_and_edges(connector, 'v1')

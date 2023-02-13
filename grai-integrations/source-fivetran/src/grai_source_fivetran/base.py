from functools import partial
from typing import List, Literal, Optional, Tuple

from grai_client.endpoints.client import BaseClient
from grai_client.schemas.edge import Edge
from grai_client.schemas.node import Node
from grai_client.update import update
from grai_source_fivetran.adapters import adapt_to_client
from grai_source_fivetran.loader import FivetranAPI

# def get_nodes_and_edges(
#     connector: FivetranConnector, version: Literal["v1"]
# ) -> Tuple[List[Node], List[Edge]]:
#     nodes, edges = connector.get_nodes_and_edges()
#
#     nodes = adapt_to_client(nodes, version)
#     edges = adapt_to_client(edges, version)
#     return nodes, edges
#
#
# def update_server(
#     client: BaseClient,
#     namespace: Optional[str] = None,
#     user: Optional[str] = None,
#     password: Optional[str] = None,
#     fivetran_endpoint: Optional[str] = None,
# ):
#     kwargs = {"user": user, "password": password}
#     if fivetran_endpoint is not None:
#         kwargs["fivetran_endpoint"] = fivetran_endpoint
#
#     conn = FivetranConnector(**kwargs)
#     nodes, edges = get_nodes_and_edges(conn, client.id)
#     update(client, nodes)
#     update(client, edges)

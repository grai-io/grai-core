from typing import List, Literal, Optional, Tuple

from grai_client.endpoints.client import BaseClient
from grai_client.schemas.edge import Edge
from grai_client.schemas.node import Node
from grai_client.update import update

from grai_source_flat_file.adapters import adapt_to_client
from grai_source_flat_file.loader import get_nodes_and_edges


def update_server(
    client: BaseClient,
    file_name: str,
    namespace: Optional[str] = None,
):
    nodes, edges = get_nodes_and_edges(file_name, namespace)
    nodes = adapt_to_client(nodes)

    update(client, nodes)
    # update(client, edges)

from grai_client.schemas.node import Node
from typing import List
import requests


def update(nodes: List[Node], active_nodes: List[Node]):
    current_nodes = {hash(node): node for node in active_nodes}
    nodes = {hash(node): node for node in nodes}

    new_nodes = nodes.items() - current_nodes.items()
    deactivated_nodes = current_nodes.items() - nodes.items()
    updated_nodes = nodes.items() - new_nodes


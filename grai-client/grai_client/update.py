from typing import Dict, List

import requests
from grai_client.schemas.node import Node
from grai_client.schemas.schema import GraiType
from grai_client.schemas.utilities import merge_models
from grai_client.endpoints.client import BaseClient


def deactivate_nodes(nodes: List[GraiType]) -> List[GraiType]:
    for node in nodes:
        node.spec.is_active = False
    return nodes


def update(client: BaseClient, nodes: List[Node], active_nodes: List[Node]):
    current_node_map = {hash(node): node for node in active_nodes}
    node_map = {hash(node): node for node in nodes}

    new_node_keys = node_map.keys() - current_node_map.keys()
    deactivated_node_keys = current_node_map.keys() - node_map.keys()
    updated_node_keys = node_map.keys() - new_node_keys

    deactivated_nodes = deactivate_nodes(
        [current_node_map[k] for k in deactivated_node_keys]
    )
    new_nodes = [node_map[k] for k in new_node_keys]
    updated_nodes = [
        merge_models(a, b) for k in updated_node_keys
        if (a := node_map[k]) != (b := current_node_map[k])
    ]

    client.patch(deactivated_nodes)
    client.patch(updated_nodes)
    client.post(new_nodes)

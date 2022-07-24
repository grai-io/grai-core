from grai_client.schemas.node import Node
from typing import List, Dict
import requests
from grai_client.schemas.schema import GraiType

from grai_client.schemas.utilities import merge_models


def deactivate_nodes(nodes: List[GraiType]) -> List[GraiType]:
    for node in nodes:
        node.spec.is_active = False
    return nodes


def patch_nodes(nodes: List[GraiType]):
    pass


def update(client, nodes: List[Node], active_nodes: List[Node]):
    current_node_map = {hash(node): node for node in active_nodes}
    node_map = {hash(node): node for node in nodes}

    new_node_keys = node_map.keys() - current_node_map.keys()
    deactivated_node_keys = current_node_map.keys() - node_map.keys()
    updated_node_keys = node_map.keys() - new_node_keys

    deactivated_nodes = deactivate_nodes([current_node_map[k] for k in deactivated_node_keys])
    new_nodes = [node_map[k] for k in new_node_keys]
    updated_nodes = [merge_models(node_map[k], current_node_map[k]) for k in updated_node_keys]

    for node in updated_nodes:
        client.patch(node)

    for node in deactivated_nodes:
        client.patch(node)

    for node in new_nodes:
        client.post(node)

import json
from typing import Any, Dict, Type

import requests
from grai_client.endpoints.utilities import (GraiEncoder,
                                             response_status_checker)
from grai_client.endpoints.v1.client import ClientV1
from grai_client.endpoints.v1.get import get_edge_node_id
from grai_client.schemas.edge import EdgeNodeValues, EdgeType, EdgeV1
from grai_client.schemas.node import NodeType, NodeV1


@ClientV1.delete.register
@response_status_checker
def delete_url(client: ClientV1, url: str) -> requests.Response:
    headers = client.auth_headers
    response = requests.delete(url, headers=headers)
    return response


@ClientV1.delete.register
def delete_node_v1(client: ClientV1, grai_type: NodeV1) -> Dict:
    node_id = grai_type.spec.id
    if node_id is None:
        node = client.get(grai_type)
        node_id = node[0]["id"]
    url = f"{client.node_endpoint}{node_id}/"
    return client.delete(url)


@ClientV1.delete.register
def delete_edge_v1(client: ClientV1, grai_type: EdgeV1) -> Dict:
    edge = client.get(grai_type)
    if len(edge) == 0:
        print(f"No edge matching `{grai_type}`")
        return {}

    edge_id = edge[0]["id"]
    url = f"{client.edge_endpoint}{edge_id}/"
    return client.delete(url)

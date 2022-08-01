import json
from functools import singledispatch
from typing import Any, Dict, Type
from uuid import UUID

import requests
from grai_client.endpoints.utilities import response_status_check, GraiEncoder
from grai_client.endpoints.v1.client import ClientV1
from grai_client.endpoints.v1.get import get_edge_node_id
from grai_client.schemas.edge import EdgeNodeValues, EdgeV1
from grai_client.schemas.node import NodeV1


@ClientV1.post.register
def post_url_v1(client: ClientV1, url: str, payload: Dict) -> requests.Response:
    headers = {**client.auth_headers, "Content-Type": "application/json"}
    payload = {k: v for k, v in payload.items() if v is not None}
    response = requests.post(url, data=json.dumps(payload, cls=GraiEncoder), headers=headers)
    response_status_check(response)
    return response


@ClientV1.post.register
def post_node_v1(client: ClientV1, grai_type: NodeV1) -> NodeV1:
    url = client.node_endpoint
    response = client.post(url, grai_type.spec.dict())
    return NodeV1.from_spec(response.json())


@ClientV1.post.register
def post_edge_v1(client: ClientV1, grai_type: EdgeV1) -> EdgeV1:
    update = {
        'source': get_edge_node_id(client, grai_type.spec.source),
        'destination': get_edge_node_id(client, grai_type.spec.destination)
    }

    url = client.edge_endpoint
    grai_type = grai_type.update({"spec": update})
    response = client.post(url, grai_type.spec.dict())
    return EdgeV1.from_spec(response.json())

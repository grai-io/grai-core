from grai_client.schemas.edge import EdgeV1, EdgeType, EdgeNodeValues
from grai_client.schemas.node import NodeV1, NodeType
from grai_client.endpoints.v1.client import ClientV1
from grai_client.endpoints.utilities import response_status_checker
from grai_client.endpoints.v1.get import get_edge_node_id
from typing import Any, Dict, Type
import requests
from uuid import UUID
import json
from functools import singledispatch


@ClientV1.post.register
@response_status_checker
def post_url_v1(client: ClientV1, url: str, payload: Dict) -> requests.Response:
    headers = client.auth_headers | {"Content-Type": "application/json"}
    payload = {k: v for k, v in payload.items() if v is not None}
    response = requests.post(url, data=json.dumps(payload), headers=headers)
    return response


@ClientV1.post.register
def post_node_v1(client: ClientV1, grai_type: NodeV1) -> Dict:
    url = client.node_endpoint
    return client.post(url, grai_type.spec.dict())


@ClientV1.post.register
def post_edge_v1(client: ClientV1, grai_type: EdgeV1) -> Dict:
    grai_type.spec.source = get_edge_node_id(grai_type.spec.source, client)
    grai_type.spec.destination = get_edge_node_id(grai_type.spec.destination, client)
    url = client.edge_endpoint
    result = grai_type.spec.dict()
    return client.post(url, result)

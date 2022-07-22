from grai_client.schemas.edge import EdgeV1, EdgeType, EdgeNodeValues
from grai_client.schemas.node import NodeV1, NodeType
from grai_client.endpoints.v1.client import ClientV1
from grai_client.endpoints.utilities import response_status_checker, GraiEncoder
from grai_client.endpoints.v1.get import get_edge_node_id
from typing import Any, Dict, Type
import requests
import json


@ClientV1.patch.register(str)
@response_status_checker
def _(client: ClientV1, url: str, payload: Dict) -> Dict:
    headers = client.auth_headers | {"Content-Type": "application/json"}
    payload = {k: v for k, v in payload.items() if v is not None}
    response = requests.patch(url, data=json.dumps(payload, cls=GraiEncoder), headers=headers)
    return response


@ClientV1.patch.register(NodeV1)
def _(client: ClientV1, grai_type: NodeV1) -> Dict:
    if grai_type.spec.id is None:
        raise Exception(f"Missing node id on {grai_type}")
    url = f'{client.node_endpoint}{grai_type.spec.id}/'
    return client.patch(url, grai_type.spec.dict())


@ClientV1.patch.register(EdgeV1)
def _(client: ClientV1, grai_type: EdgeV1) -> Dict:
    grai_type.spec.source = get_edge_node_id(grai_type.spec.source, client)
    grai_type.spec.destination = get_edge_node_id(grai_type.spec.destination, client)
    url = client.edge_endpoint
    result = grai_type.spec.dict()
    return client.patch(url, result)



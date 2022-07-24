import json
from typing import Any, Dict, Type

import requests
from grai_client.endpoints.utilities import (GraiEncoder,
                                             response_status_checker)
from grai_client.endpoints.v1.client import ClientV1
from grai_client.endpoints.v1.get import get_edge_node_id
from grai_client.schemas.edge import EdgeNodeValues, EdgeType, EdgeV1
from grai_client.schemas.node import NodeType, NodeV1


@ClientV1.patch.register
@response_status_checker
def patch_url_v1(client: ClientV1, url: str, payload: Dict) -> requests.Response:
    headers = client.auth_headers | {"Content-Type": "application/json"}
    payload = {k: v for k, v in payload.items() if v is not None}
    response = requests.patch(
        url, data=json.dumps(payload, cls=GraiEncoder), headers=headers
    )
    return response


@ClientV1.patch.register
def patch_node_v1(client: ClientV1, grai_type: NodeV1) -> Dict:
    if grai_type.spec.id is None:
        raise Exception(f"Missing node id on {grai_type}")
    url = f"{client.node_endpoint}{grai_type.spec.id}/"
    return client.patch(url, grai_type.spec.dict())


@ClientV1.patch.register
def patch_edge_v1(client: ClientV1, grai_type: EdgeV1) -> Dict:
    grai_type.spec.source = get_edge_node_id(grai_type.spec.source, client)
    grai_type.spec.destination = get_edge_node_id(grai_type.spec.destination, client)
    url = client.edge_endpoint
    result = grai_type.spec.dict()
    return client.patch(url, result)

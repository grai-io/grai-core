import json
from typing import Any, Dict, Type

import requests
from grai_client.endpoints.utilities import (GraiEncoder,
                                             response_status_check)
from grai_client.endpoints.v1.client import ClientV1
from grai_client.endpoints.v1.get import get_edge_node_id
from grai_client.schemas.edge import EdgeNodeValues, EdgeV1
from grai_client.schemas.node import  NodeV1


@ClientV1.patch.register
def patch_url_v1(client: ClientV1, url: str, payload: Dict) -> requests.Response:
    headers = {**client.auth_headers, "Content-Type": "application/json"}
    payload = {k: v for k, v in payload.items() if v is not None}
    response = requests.patch(
        url, data=json.dumps(payload, cls=GraiEncoder), headers=headers
    )

    response_status_check(response)
    return response


@ClientV1.patch.register
def patch_node_v1(client: ClientV1, grai_type: NodeV1) -> NodeV1:
    if grai_type.spec.id is None:
        raise Exception(f"Missing node id on {grai_type}")
    url = f"{client.node_endpoint}{grai_type.spec.id}/"
    response = client.patch(url, grai_type.spec.dict())
    return NodeV1.from_spec(response.json())


@ClientV1.patch.register
def patch_edge_v1(client: ClientV1, grai_type: EdgeV1) -> EdgeV1:
    update = {
        'source': get_edge_node_id(client, grai_type.spec.source),
        'destination': get_edge_node_id(client, grai_type.spec.destination)
    }

    url = f"{client.edge_endpoint}{grai_type.spec.id}/"
    grai_type = grai_type.update({"spec": update})
    response = client.patch(url, grai_type.spec.dict())
    return EdgeV1.from_spec(response.json())

import json
from typing import Any, Dict, List, Optional, Type

import requests
from grai_client.endpoints.client import ClientOptions, delete
from grai_client.endpoints.utilities import GraiEncoder, response_status_check
from grai_client.endpoints.v1.client import ClientV1
from grai_client.schemas.edge import EdgeV1
from grai_client.schemas.node import NodeV1


@delete.register
def delete_node_v1(
    client: ClientV1, grai_type: NodeV1, options: ClientOptions = ClientOptions()
):
    if grai_type.spec.id is None:
        grai_type = client.get(grai_type, options)
        if grai_type is None:
            return
    url = f"{client.node_endpoint}{grai_type.spec.id}/"
    client.delete(url, options)


@delete.register
def delete_edge_v1(
    client: ClientV1, grai_type: EdgeV1, options: ClientOptions = ClientOptions()
):
    if grai_type.spec.id is None:
        grai_type = client.get(grai_type, options)
        if grai_type is None:
            return
    url = f"{client.edge_endpoint}{grai_type.spec.id}/"
    client.delete(url, options)

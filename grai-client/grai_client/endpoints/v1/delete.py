import json
from typing import Any, Dict, Type, List

import requests
from grai_client.endpoints.utilities import (GraiEncoder,
                                             response_status_check)
from grai_client.endpoints.v1.client import ClientV1
from grai_client.schemas.edge import EdgeV1
from grai_client.schemas.node import NodeV1


@ClientV1.delete.register
def delete_node_v1(client: ClientV1, grai_type: NodeV1):
    if grai_type.spec.id is None:
        grai_type = client.get(grai_type)
    url = f"{client.node_endpoint}{grai_type.spec.id}/"
    client.delete(url)


@ClientV1.delete.register
def delete_edge_v1(client: ClientV1, grai_type: EdgeV1):
    print('in delete edge')
    if grai_type.spec.id is None:
        grai_type = client.get(grai_type)
    url = f"{client.edge_endpoint}{grai_type.spec.id}/"
    client.delete(url)
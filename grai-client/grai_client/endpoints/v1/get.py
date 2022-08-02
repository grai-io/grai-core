from typing import Any, Union, Literal, List, Optional, TypeVar
from uuid import UUID

import requests
from grai_client.endpoints.utilities import response_status_check
from grai_client.endpoints.v1.client import ClientV1
from grai_client.schemas.edge import EdgeLabels, EdgeV1, NodeID
from grai_client.schemas.node import NodeLabels, NodeV1
from multimethod import multimethod
from itertools import chain


T = TypeVar("T", NodeV1, EdgeV1)


@ClientV1.get.register
def get_node_id(client: ClientV1, grai_type: NodeID) -> Optional[NodeID]:
    base_url = client.node_endpoint
    if grai_type.id:
        return grai_type

    url = f"{base_url}?name={grai_type.name}&namespace={grai_type.namespace}"
    resp = client.get(url).json()
    if len(resp) == 0:
        return None
    spec = NodeV1.from_spec(resp[0]).spec
    return NodeID(id=spec.id, name=spec.name, namespace=spec.namespace)


@ClientV1.get.register
def get_node_v1(client: ClientV1, grai_type: NodeV1) -> Optional[NodeV1]:
    base_url = client.node_endpoint
    if grai_type.spec.id is not None:
        url = f"{base_url}{grai_type.spec.id}"
        resp = client.get(url).json()
    else:
        url = f"{base_url}?name={grai_type.spec.name}&namespace={grai_type.spec.namespace}"
        resp = client.get(url).json()
        if len(resp) == 0:
            return None
        resp = resp[0]
    return NodeV1.from_spec(resp)


@ClientV1.get.register
def get_node_by_label_v1(client: ClientV1, grai_type: NodeLabels) -> List[NodeV1]:
    url = client.get_url(grai_type)
    resp = client.get(url).json()
    return [NodeV1.from_spec(obj) for obj in resp]


@ClientV1.get.register
def get_node_by_id(client: ClientV1, grai_type: NodeLabels, node: str) -> Optional[NodeV1]:
    url = f"{client.node_endpoint}{node}"
    resp = client.get(url).json()
    return NodeV1.from_spec(resp)


@ClientV1.get.register
def get_edge_v1(client: ClientV1, grai_type: EdgeV1) -> Optional[EdgeV1]:
    base_url = client.edge_endpoint
    if grai_type.spec.id is not None:
        url = f"{base_url}{grai_type.spec.id}"
        resp = client.get(url).json()
    else:
        url = f"{base_url}?name={grai_type.spec.name}&namespace={grai_type.spec.namespace}"
        resp = client.get(url).json()
        if len(resp) == 0:
            return None
        resp = resp[0]


    resp['source'] = client.get('node', resp['source']).spec
    resp['destination'] = client.get('node', resp['destination']).spec
    return EdgeV1.from_spec(resp)


@ClientV1.get.register
def get_edge_by_label_v1(client: ClientV1, grai_type: EdgeLabels) -> List[EdgeV1]:
    url = client.get_url(grai_type)
    resp = client.get(url).json()

    for r in resp:
        r['source'] = client.get('node', r['source']).spec
        r['destination'] = client.get('node', r['destination']).spec

    return [EdgeV1.from_spec(obj) for obj in resp]

from itertools import chain
from typing import Any, Dict, List, Literal, Optional, Type, TypeVar, Union
from uuid import UUID

import requests
from grai_client.endpoints.client import ClientOptions, get
from grai_client.endpoints.v1.client import ClientV1
from grai_client.schemas.edge import EdgeLabels, EdgeV1, NodeID
from grai_client.schemas.node import NodeLabels, NodeV1

T = TypeVar("T", NodeV1, EdgeV1)


def get_node_from_id(
    client: ClientV1,
    grai_type: NodeID,
    options: Optional[ClientOptions] = ClientOptions(),
) -> Optional[Dict]:
    base_url = client.get_url(grai_type)
    if grai_type.id is not None:
        url = f"{base_url}{grai_type.id}"
        resp = client.get(url).json()
    else:
        url = f"{base_url}?name={grai_type.name}&namespace={grai_type.namespace}"
        resp = client.get(url, options).json()
        num_results = len(resp)
        if num_results == 0:
            return None
        elif num_results == 1:
            resp = resp[0]
        else:
            message = (
                f"Server query for node returned {num_results} results but only one was expected. This "
                f"is a defensive error that should never arise, if you see it please contact the maintainers."
            )
            raise Exception(message)

    return resp


@get.register
def get_node_id(
    client: ClientV1, grai_type: NodeID, options: ClientOptions = ClientOptions()
) -> Optional[NodeID]:
    spec = get_node_from_id(client, grai_type, options)
    return NodeV1.from_spec(spec).spec if isinstance(spec, dict) else spec


@get.register
def get_node_v1(
    client: ClientV1, grai_type: NodeV1, options: ClientOptions = ClientOptions()
) -> Optional[NodeV1]:
    spec = get_node_from_id(client, grai_type.spec, options)
    return NodeV1.from_spec(spec) if isinstance(spec, dict) else spec


@get.register
def get_node_by_label_v1(
    client: ClientV1, grai_type: NodeLabels, options: ClientOptions = ClientOptions()
) -> List[NodeV1]:
    url = client.node_endpoint
    resp = client.get(url, options).json()
    return [NodeV1.from_spec(obj) for obj in resp]


@get.register
def get_node_by_id(
    client: ClientV1,
    grai_type: NodeLabels,
    node: str,
    options: ClientOptions = ClientOptions(),
) -> Optional[NodeV1]:
    url = f"{client.node_endpoint}{node}"
    resp = client.get(url, options).json()
    return NodeV1.from_spec(resp)


@get.register
def get_edge_v1(
    client: ClientV1, grai_type: EdgeV1, options: ClientOptions = ClientOptions()
) -> Optional[EdgeV1]:
    base_url = client.edge_endpoint
    if grai_type.spec.id is not None:
        url = f"{base_url}{grai_type.spec.id}"
        resp = client.get(url, options).json()
    else:
        url = f"{base_url}?name={grai_type.spec.name}&namespace={grai_type.spec.namespace}"
        resp = client.get(url, options).json()
        if len(resp) == 0:
            return None
        resp = resp[0]

    resp["source"] = client.get("node", resp["source"]).spec
    resp["destination"] = client.get("node", resp["destination"]).spec
    return EdgeV1.from_spec(resp)


@get.register
def get_edge_by_label_v1(
    client: ClientV1, grai_type: EdgeLabels, options: ClientOptions = ClientOptions()
) -> List[EdgeV1]:
    url = client.get_url(grai_type)
    resp = client.get(url, options).json()

    for r in resp:
        r["source"] = client.get("node", r["source"], options).spec
        r["destination"] = client.get("node", r["destination"], options).spec

    return [EdgeV1.from_spec(obj) for obj in resp]

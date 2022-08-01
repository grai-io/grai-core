from typing import Any, Union, Literal, List, Optional
from uuid import UUID

import requests
from grai_client.endpoints.utilities import response_status_check, list_response_parser, response_parser
from grai_client.endpoints.v1.client import ClientV1
from grai_client.schemas.edge import EdgeNodeValues, EdgeLabels, EdgeV1
from grai_client.schemas.node import NodeLabels, NodeV1
from multimethod import multimethod


@multimethod
def get_edge_node_id(client: ClientV1, node_id: Any) -> UUID:
    raise NotImplementedError(f"No get method implemented for type {type(node_id)}")


@get_edge_node_id.register
def get_edge_node_by_id_v1(client: ClientV1, node_id: UUID) -> UUID:
    return node_id


@get_edge_node_id.register
def get_edge_node_v1(client: ClientV1, node_id: EdgeNodeValues) -> UUID:
    node: NodeV1 = client.get(node_id)
    return node.spec.id


@ClientV1.get.register
def get_url_v1(client: ClientV1, url: str) -> requests.Response:
    response = requests.get(url, headers=client.auth_headers)
    response_status_check(response)
    return response


def url_with_filters(url: str, node: NodeV1) -> str:
    keys = ["name", "namespace"]
    filters = "&".join([f"{key}={getattr(node.spec, key)}" for key in keys])
    return f"{url}?{filters}"


@ClientV1.get.register
def get_specific_node_v1(client: ClientV1, grai_type: NodeV1) -> Optional[NodeV1]:
    url = url_with_filters(client.node_endpoint, grai_type)
    resp = client.get(url).json()
    if len(resp) == 0:
        print(f"No node found matching {grai_type}")
        return
    return NodeV1.from_spec(resp[0])


@ClientV1.get.register
def get_node_by_label_v1(client: ClientV1, grai_type: NodeLabels) -> List[NodeV1]:
    url = client.node_endpoint
    resp = client.get(url).json()
    return [NodeV1.from_spec(obj) for obj in resp]


@ClientV1.get.register
def get_node_by_names_v1(
    client: ClientV1, node_values: EdgeNodeValues
) -> NodeV1:
    url = f"{client.node_endpoint}?name={node_values.name}&namespace={node_values.namespace}"
    resp = client.get(url).json()
    return NodeV1.from_spec(resp[0])


@ClientV1.get.register
def get_edge_by_label_v1(
    client: ClientV1, grai_type: EdgeLabels
) -> List[EdgeV1]:
    url = client.edge_endpoint
    resp = client.get(url).json()
    return [EdgeV1.from_spec(obj) for obj in resp]


def edge_url_with_filters(client: ClientV1, edge: EdgeV1) -> str:
    source = get_edge_node_id(client, edge.spec.source)
    destination = get_edge_node_id(client, edge.spec.destination)
    return f"{client.edge_endpoint}?source={source}&destination={destination}"


@ClientV1.get.register
def get_edge_v1(
    client: ClientV1, grai_type: EdgeV1
) -> Optional[EdgeV1]:
    url = edge_url_with_filters(client, grai_type)
    print(url)
    resp = client.get(url).json()
    if len(resp) == 0:
        print(f"No edge found matching {grai_type}")
        return
    return EdgeV1.from_spec(resp[0])

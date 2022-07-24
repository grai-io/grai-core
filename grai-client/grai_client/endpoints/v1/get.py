from functools import singledispatch
from typing import Any, Union
from uuid import UUID

import requests
from grai_client.endpoints.utilities import response_status_checker
from grai_client.endpoints.v1.client import ClientV1
from grai_client.schemas.edge import EdgeNodeValues, EdgeType, EdgeV1
from grai_client.schemas.node import NodeType, NodeV1


@singledispatch
def get_edge_node_id(node_id: Any, client: ClientV1) -> UUID:
    raise NotImplementedError(f"No get method implemented for type {type(node_id)}")


@get_edge_node_id.register
def get_edge_node_by_id_v1(node_id: UUID, client: ClientV1) -> UUID:
    return node_id


@get_edge_node_id.register
def get_edge_node_v1(node_id: EdgeNodeValues, client: ClientV1) -> UUID:
    node = client.get(node_id)
    if len(node) == 0:
        message = f"No node found matching (name={node_id.name}, namespace={node_id.namespace})"
        raise ValueError(message)
    elif len(node) > 1:
        message = (
            f"Something awful has happened there should only be one node matching (name={node_id.name}, namespace={node_id.namespace})."
            "This is likely a bug, pleaase create an issue report at https://github.com/grai-io/grai-core/issues"
        )
        raise Exception(message)

    return node[0]["id"]


@ClientV1.get.register
@response_status_checker
def get_url_v1(client: ClientV1, url: str) -> requests.Response:
    response = requests.get(url, headers=client.auth_headers)
    return response


def url_with_filters(url: str, node: NodeV1) -> str:
    keys = ["name", "namespace"]
    filters = "&".join([f"{key}={getattr(node.spec, key)}" for key in keys])
    return f"{url}?{filters}"


@ClientV1.get.register
def get_specific_node_v1(client: ClientV1, grai_type: NodeV1) -> requests.Response:
    url = url_with_filters(client.node_endpoint, grai_type)
    return client.get(url)


@ClientV1.get.register
def get_node_v1(client: ClientV1, grai_type: NodeType) -> requests.Response:
    url = client.node_endpoint
    return client.get(url)


@ClientV1.get.register
def get_node_by_names_v1(
    client: ClientV1, node_values: EdgeNodeValues
) -> requests.Response:
    url = f"{client.node_endpoint}?name={node_values.name}&namespace={node_values.namespace}"
    return client.get(url)


@ClientV1.get.register
def get_edge_v1(
    client: ClientV1, grai_type: Union[EdgeType, EdgeV1]
) -> requests.Response:
    url = client.edge_endpoint
    return client.get(url)

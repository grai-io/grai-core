from grai_client.schemas.edge import EdgeV1, EdgeType, EdgeNodeValues
from grai_client.schemas.node import NodeV1, NodeType
from grai_client.endpoints.v1.client import ClientV1
from grai_client.endpoints.utilities import response_status_checker
import requests
from functools import singledispatch
from typing import Union, Any
from uuid import UUID


@singledispatch
def get_edge_node_id(node_id: Any, client: ClientV1) -> UUID:
    raise NotImplementedError(f"No post method implemented for type {type(node_id)}")


@get_edge_node_id.register
def _(node_id: UUID, client: ClientV1) -> UUID:
    return node_id


@get_edge_node_id.register
def _(node_id: EdgeNodeValues, client: ClientV1) -> UUID:
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


@ClientV1.get.register(str)
@response_status_checker
def _(client: ClientV1, url: str) -> requests.request:
    response = requests.get(url, headers=client.auth_headers)
    return response


def url_with_filters(url: str, node: NodeV1) -> str:
    keys = ['name', 'namespace']
    filters = "&".join([f"{key}={getattr(node.spec, key)}" for key in keys])
    return f"{url}?{filters}"


@ClientV1.get.register(NodeV1)
def _(client: ClientV1, grai_type: NodeV1) -> requests.request:
    url = url_with_filters(client.node_endpoint, grai_type)
    return client.get(url)


@ClientV1.get.register(NodeType)
def _(client: ClientV1, grai_type: NodeType) -> requests.request:
    url = client.node_endpoint
    return client.get(url)


@ClientV1.get.register(EdgeNodeValues)
def _(client: ClientV1, node_values: EdgeNodeValues) -> requests.request:
    url = f"{client.node_endpoint}?name={node_values.name}&namespace={node_values.namespace}"
    return client.get(url)


@ClientV1.get.register(EdgeV1)
@ClientV1.get.register(EdgeType)
def _(client: ClientV1, grai_type: EdgeV1) -> requests.request:
    url = client.edge_endpoint
    return client.get(url)

from grai_client.schemas.edge import EdgeV1, EdgeType, EdgeNodeValues
from grai_client.schemas.node import NodeV1, NodeType
from grai_client.endpoints.v1.client import ClientV1
from typing import Any, Dict, Type
import requests
from uuid import UUID
import json
from functools import singledispatch


@singledispatch
def get_edge_node_id(node_id: Any, client: ClientV1) -> UUID:
    raise NotImplementedError(f"No post method implemented for type {type(node_id)}")


@get_edge_node_id.register
def _(node_id: UUID, client: ClientV1) -> UUID:
    return node_id


@get_edge_node_id.register
def _(node_id: EdgeNodeValues, client: ClientV1) -> UUID:
    node = client.get(node_id)
    # if len(node) == 0:
    #     typer.echo(f"No node found matching (name={node_id.name}, namespace={node_id.namespace})")
    #     raise typer.Exit()
    # elif len(node) > 1:
    #     message = (
    #         f"Something awful has happened there should only be one node matching (name={node_id.name}, namespace={node_id.namespace})."
    #         "This is likely a bug, pleaase create an issue report at https://github.com/grai-io/grai-core/issues"
    #     )
    #     typer.echo(message)
    #     raise typer.Exit()

    return node[0]['id']


@ClientV1.post.register(str)
def _(client: ClientV1, url: str, payload: Dict) -> Dict:
    headers = client.authentication_headers() | {'Content-Type': 'application/json'}
    payload = {k: v for k, v in payload.items() if v is not None}
    response = requests.post(url, data=json.dumps(payload), headers=headers)
    return response


@ClientV1.post.register(NodeV1)
def _(client: ClientV1, grai_type: NodeV1) -> Dict:
    url = client.node_endpoint
    return client.post(url, grai_type.spec.dict())


@ClientV1.post.register(EdgeV1)
def _(client: ClientV1, grai_type: EdgeV1) -> Dict:
    grai_type.spec.source = get_edge_node_id(grai_type.spec.source, client)
    grai_type.spec.destination = get_edge_node_id(grai_type.spec.destination, client)
    url = client.edge_endpoint
    result = grai_type.spec.dict()
    return client.post(url, result)

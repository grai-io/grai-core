from typing import Optional, TypeVar

from grai_client.endpoints.client import ClientOptions
from grai_client.endpoints.rest import patch
from grai_client.endpoints.v1.client import ClientV1
from grai_client.endpoints.v1.utils import process_node_id
from grai_client.schemas import edge, node

T = TypeVar("T", node.NodeV1, edge.EdgeV1)


@patch.register
def patch_node_v1(
    client: ClientV1, grai_type: node.NodeV1, options: ClientOptions = ClientOptions()
) -> Optional[node.NodeV1]:
    if grai_type.spec.id is None:
        current = client.get(grai_type)
        grai_type.spec.id = current.spec.id

    url = f"{client.get_url(grai_type)}{grai_type.spec.id}/"
    response = client.patch(
        url, grai_type.spec.dict(exclude_none=True), options=options
    ).json()
    if response is None:
        return None
    return node.NodeV1.from_spec(response)


@patch.register
def patch_edge_v1(
    client: ClientV1, grai_type: edge.EdgeV1, options: ClientOptions = ClientOptions()
) -> Optional[edge.EdgeV1]:
    if grai_type.spec.id is None:
        current = client.get(grai_type)
        grai_type.spec.id = current.spec.id

    url = f"{client.get_url(grai_type)}{grai_type.spec.id}/"

    source = process_node_id(client, grai_type.spec.source)
    destination = process_node_id(client, grai_type.spec.destination)

    payload = grai_type.spec.dict(exclude_none=True)
    payload["source"] = source.id
    payload["destination"] = destination.id

    response = client.patch(url, payload, options=options).json()
    if response is None:
        return None

    response["source"] = source
    response["destination"] = destination
    return edge.EdgeV1.from_spec(response)

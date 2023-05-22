import asyncio
from typing import Optional, TypeVar

from grai_schemas.v1 import EdgeV1, NodeV1

from grai_client.endpoints.client import ClientOptions
from grai_client.endpoints.rest import get, patch
from grai_client.endpoints.v1.client import ClientV1
from grai_client.endpoints.v1.get import finalize_edge
from grai_client.endpoints.v1.utils import process_node_id

T = TypeVar("T", NodeV1, EdgeV1)


@patch.register
async def patch_node_v1(
    client: ClientV1, grai_type: NodeV1, options: ClientOptions = ClientOptions()
) -> Optional[NodeV1]:
    if grai_type.spec.id is None:
        current = await get(client, grai_type)
        grai_type.spec.id = current.spec.id

    url = f"{client.get_url(grai_type)}{grai_type.spec.id}/"
    response = await patch(client, url, grai_type.spec.dict(exclude_none=True), options=options)
    response = response.json()
    if response is None:
        return None
    return NodeV1.from_spec(response)


@patch.register
async def patch_edge_v1(
    client: ClientV1, grai_type: EdgeV1, options: ClientOptions = ClientOptions()
) -> Optional[EdgeV1]:
    if grai_type.spec.id is None:
        current = await get(client, grai_type)
        grai_type.spec.id = current.spec.id

    source, destination = await asyncio.gather(
        process_node_id(client, grai_type.spec.source, options),
        process_node_id(client, grai_type.spec.destination, options),
    )

    payload = {**grai_type.spec.dict(exclude_none=True), "source": source.id, "destination": destination.id}

    url = f"{client.get_url(grai_type)}{grai_type.spec.id}/"
    response = await patch(client, url, payload, options=options)
    response = response.json()
    if response is None:
        return None

    response["source"] = source
    response["destination"] = destination
    return EdgeV1.from_spec(response)

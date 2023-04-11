import asyncio
from typing import Dict, List, Literal, Optional, TypeVar, Union

from grai_schemas.v1 import EdgeV1, NodeV1
from grai_schemas.v1.node import NodeIdTypes, NodeNamedID, NodeUuidID

from grai_client.endpoints.client import ClientOptions
from grai_client.endpoints.rest import get
from grai_client.endpoints.utilities import is_valid_uuid
from grai_client.endpoints.v1.client import ClientV1
from grai_client.schemas.labels import EdgeLabels, NodeLabels, WorkspaceLabels
from grai_client.schemas.workspace import Workspace

T = TypeVar("T", NodeV1, EdgeV1)
X = TypeVar("X")


async def query_obj_from_param_string(
    client: ClientV1, base_url: str, options=ClientOptions(), **kwargs
) -> Optional[List[Dict]]:
    supported_params = ["name", "namespace"]
    query = "&".join([f"{param}={kwargs[param]}" for param in supported_params if param in kwargs])

    url = f"{base_url}?{query}"
    resp = await get(client, url, options=options)
    resp = resp.json()

    num_results = len(resp)
    if num_results == 0:
        return None
    else:
        return resp


async def get_node_from_id(
    client: ClientV1,
    grai_type: NodeIdTypes,
    options: Optional[ClientOptions] = ClientOptions(),
) -> Optional[Dict]:
    base_url = client.get_url(grai_type)
    if grai_type.id is not None:
        url = f"{base_url}{grai_type.id}/"
        resp = await get(client, url, options=options)
        resp = resp.json()
    else:
        resp = await query_obj_from_param_string(
            client, base_url, options=options, name=grai_type.name, namespace=grai_type.namespace
        )

        if resp is None:
            return None
        elif len(resp) == 1:
            return resp[0]
        else:
            message = (
                f"Server query for node returned {len(resp)} results but only one was expected. This "
                f"is a defensive error that should never arise, if you see it please contact the maintainers."
            )
            raise Exception(message)

    return resp


@get.register
async def get_from_node_id(
    client: ClientV1, grai_type: NodeIdTypes, options: ClientOptions = ClientOptions()
) -> Optional[NodeV1]:
    spec = await get_node_from_id(client, grai_type, options=options)
    return NodeV1.from_spec(spec) if isinstance(spec, dict) else spec


@get.register
async def get_node_v1(
    client: ClientV1, grai_type: NodeV1, options: ClientOptions = ClientOptions()
) -> Optional[NodeV1]:
    spec = await get_node_from_id(client, grai_type.spec, options)
    return NodeV1.from_spec(spec) if isinstance(spec, dict) else spec


async def _get_nodes_by_name(
    client: ClientV1,
    grai_type: NodeLabels,
    name: str,
    options: ClientOptions = ClientOptions(),
) -> Optional[List[NodeV1]]:
    url = f"{client.get_url(grai_type)}?name={name}"
    resp = await get(client, url, options=options)
    resp = resp.json()
    num_results = len(resp)
    if num_results == 0:
        return None
    else:
        return [NodeV1.from_spec(obj) for obj in resp]


async def _get_nodes_by_uuid(
    client: ClientV1,
    grai_type: NodeLabels,
    name: str,
    options: ClientOptions = ClientOptions(),
) -> Optional[NodeV1]:
    url = f"{client.get_url(grai_type)}{name}/"

    resp = await get(client, url, options=options)
    resp = resp.json()
    return NodeV1.from_spec(resp)


@get.register
async def get_nodes_by_str(
    client: ClientV1,
    grai_type: NodeLabels,
    name: str,
    options: ClientOptions = ClientOptions(),
) -> Optional[Union[List[NodeV1], NodeV1]]:
    if is_valid_uuid(name):
        return await _get_nodes_by_uuid(client, grai_type, name, options=options)
    else:
        return await _get_nodes_by_name(client, grai_type, name, options=options)


@get.register
async def get_nodes_by_namespace(
    client: ClientV1,
    grai_type: NodeLabels,
    name: Literal["*"],
    namespace: str,
    options: ClientOptions = ClientOptions(),
) -> Optional[List[NodeV1]]:
    base_url = client.get_url(grai_type)
    results = await query_obj_from_param_string(client, base_url, options=options, namespace=namespace)
    if results is None:
        return results

    return [NodeV1.from_spec(result) for result in results]


@get.register
async def get_nodes_by_name_and_namespace(
    client: ClientV1,
    grai_type: NodeLabels,
    name: str,
    namespace: str,
    options: ClientOptions = ClientOptions(),
) -> Optional[NodeV1]:
    node_id = NodeNamedID(name=name, namespace=namespace)
    return await get(client, node_id, options=options)


@get.register
async def get_node_by_label_v1(
    client: ClientV1, grai_type: NodeLabels, options: ClientOptions = ClientOptions()
) -> List[NodeV1]:
    url = client.get_url(grai_type)
    resp = await get(client, url, options=options)
    resp = resp.json()
    return [NodeV1.from_spec(obj) for obj in resp]


@get.register
async def get_edge_v1(
    client: ClientV1, grai_type: EdgeV1, options: ClientOptions = ClientOptions()
) -> Optional[EdgeV1]:
    base_url = client.get_url(grai_type)
    if grai_type.spec.id is not None:
        url = f"{base_url}{grai_type.spec.id}/"
        resp = await get(client, url, options=options)
        resp = resp.json()
    else:
        url = f"{base_url}?name={grai_type.spec.name}&namespace={grai_type.spec.namespace}"
        resp = await get(client, url, options=options)
        resp = resp.json()
        if len(resp) == 0:
            return None
        resp = resp[0]

    nodes = await asyncio.gather(get(client, "node", resp["source"]), get(client, "node", resp["destination"]))
    resp["source"] = nodes[0].spec
    resp["destination"] = nodes[1].spec
    return EdgeV1.from_spec(resp)


@get.register
async def get_edge_by_label_v1(
    client: ClientV1, grai_type: EdgeLabels, options: ClientOptions = ClientOptions()
) -> List[EdgeV1]:
    url = client.get_url(grai_type)
    resp = await get(client, url, options=options)
    resp = resp.json()

    groups = [asyncio.gather(get(client, "node", r["source"]), get(client, "node", r["destination"])) for r in resp]
    nodes_groups = await asyncio.gather(*groups)
    for r, node in zip(resp, nodes_groups):
        r["source"] = node[0].spec
        r["destination"] = node[1].spec

    return [EdgeV1.from_spec(obj) for obj in resp]


@get.register
async def get_all_workspaces(
    client: ClientV1,
    grai_type: WorkspaceLabels,
    options: ClientOptions = ClientOptions(),
) -> Optional[List[Workspace]]:
    resp = await get(client, client.get_url(grai_type), options=options)
    resp = resp.json()

    if len(resp) == 0:
        return None
    else:
        return [Workspace(**item) for item in resp]


@get.register
async def get_workspace_by_name_v1(
    client: ClientV1,
    grai_type: WorkspaceLabels,
    name: str,
    options: ClientOptions = ClientOptions(),
) -> Optional[Workspace]:
    if is_valid_uuid(name):
        url = f"{client.get_url(grai_type)}{name}/"
    elif len(name.split("/")) == 2:
        # this is a ref string i.e. org-name/workspace-name
        url = f"{client.get_url(grai_type)}?ref={name}"
    else:
        url = f"{client.get_url(grai_type)}?name={name}"
    resp = await get(client, url, options=options)
    resp = resp.json()

    num_resp = len(resp)
    if num_resp == 0:
        return None
    elif num_resp == 1:
        return Workspace(**resp[0])
    else:
        raise Exception(
            f"We were unable to identify a unique workspace matching `{name}` because more than one result was "
            f"returned. This may be the result of belonging to multiple organizations with identical workspace "
            f"names. You can narrow your query by instead providing a workspace ref composed of  "
            "{org-name}/{workspace-name}.",
        )

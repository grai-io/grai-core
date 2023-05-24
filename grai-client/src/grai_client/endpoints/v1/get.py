from typing import Dict, List, Literal, Optional, TypeVar, Union
from uuid import UUID

from grai_schemas.v1 import EdgeV1, NodeV1
from grai_schemas.v1.edge import EdgeNamedID, EdgeUuidID
from grai_schemas.v1.node import NodeNamedID, NodeUuidID

from grai_client.endpoints.client import ClientOptions
from grai_client.endpoints.rest import get
from grai_client.endpoints.utilities import is_valid_uuid
from grai_client.endpoints.v1.client import ClientV1
from grai_client.schemas.labels import EdgeLabels, NodeLabels, WorkspaceLabels
from grai_client.schemas.workspace import Workspace

T = TypeVar("T", NodeV1, EdgeV1)
X = TypeVar("X")


@get.register
def get_node_by_label_v1(
    client: ClientV1, grai_type: NodeLabels, options: ClientOptions = ClientOptions()
) -> List[NodeV1]:
    url = client.get_url(grai_type)
    resp = get(client, url, options=options)
    return [NodeV1.from_spec(obj) for obj in resp.json()]


@get.register
def get_node_v1(client: ClientV1, grai_type: NodeV1, options: ClientOptions = ClientOptions()) -> Optional[NodeV1]:
    return get(client, grai_type.spec, options)


@get.register
def get_nodes_by_uuid_str_id(
    client: ClientV1,
    grai_type: NodeLabels,
    node_uuid: Union[str, UUID],
    options: ClientOptions = ClientOptions(),
) -> NodeV1:
    if not is_valid_uuid(node_uuid):
        raise ValueError(f"The provided node id {node_uuid} is not a valid uuid.")

    url = f"{client.get_url(grai_type)}{node_uuid}/"

    resp = get(client, url, options=options)
    resp = resp.json()
    return NodeV1.from_spec(resp)


@get.register
def get_from_node_uuid_id(
    client: ClientV1, grai_type: NodeUuidID, options: ClientOptions = ClientOptions()
) -> Optional[NodeV1]:
    return get(client, "Node", grai_type.id, options=options)


@get.register
def get_from_node_named_id(
    client: ClientV1, grai_type: NodeNamedID, options: ClientOptions = ClientOptions()
) -> Optional[NodeV1]:
    options = options.copy()
    options.query_args = {**options.query_args, "name": grai_type.name, "namespace": grai_type.namespace}

    result = get(client, "Node", options=options)

    num_results = len(result)
    if num_results == 0:
        return None
    elif num_results == 1:
        return result[0]
    else:
        message = (
            f"A node query for name={grai_type.name}, namespace={grai_type.namespace} in the "
            f"workspace={options.query_args.get('workspace', '<unknown workspace>')} returned more than one result. "
            f"This is a defensive error which should not be triggered. If you encounter it "
            "please open an issue at www.github.com/grai-io/grai-core/issues"
        )
        raise Exception(message)


# ----- Edges ----- #


def finalize_edge(client: ClientV1, resp: Dict, options: ClientOptions = ClientOptions()) -> EdgeV1:
    nodes = [get(client, "node", resp["source"]), get(client, "node", resp["destination"])]
    resp["source"] = nodes[0].spec
    resp["destination"] = nodes[1].spec
    return EdgeV1.from_spec(resp)


@get.register
def get_edge_by_label_v1(
    client: ClientV1, grai_type: EdgeLabels, options: ClientOptions = ClientOptions()
) -> List[EdgeV1]:
    url = client.get_url(grai_type)
    resp = get(client, url, options=options)
    return [finalize_edge(client, edge) for edge in resp.json()]


@get.register
def get_edge_by_uuid_str_id(
    client: ClientV1,
    grai_type: EdgeLabels,
    edge_uuid: Union[str, UUID],
    options: ClientOptions = ClientOptions(),
) -> EdgeV1:
    if not is_valid_uuid(edge_uuid):
        raise ValueError(f"The provided node id {edge_uuid} is not a valid uuid.")

    url = f"{client.get_url(grai_type)}{edge_uuid}/"

    resp = get(client, url, options=options)
    return finalize_edge(client, resp.json(), options)


@get.register
def get_edge_v1(client: ClientV1, grai_type: EdgeV1, options: ClientOptions = ClientOptions()) -> Optional[EdgeV1]:
    return get(client, grai_type.spec, options)


@get.register
def get_from_edge_uuid_id(
    client: ClientV1, grai_type: EdgeUuidID, options: ClientOptions = ClientOptions()
) -> Optional[EdgeV1]:
    return get(client, "Edge", grai_type.id, options=options)


@get.register
def get_from_edge_named_id(
    client: ClientV1, grai_type: EdgeNamedID, options: ClientOptions = ClientOptions()
) -> Optional[EdgeV1]:
    options = options.copy()
    options.query_args = {**options.query_args, "name": grai_type.name, "namespace": grai_type.namespace}

    resp = get(client, "Edge", options=options)

    num_results = len(resp)
    if num_results == 0:
        return None
    elif num_results == 1:
        return finalize_edge(client, resp[0])
    else:
        message = (
            f"An edge query for name={grai_type.name}, namespace={grai_type.namespace} in the "
            f"workspace={options.query_args.get('workspace', '<unknown workspace>')} returned more than one result. "
            f"This is a defensive error which should not be triggered. If you encounter it "
            "please open an issue at www.github.com/grai-io/grai-core/issues"
        )
        raise Exception(message)


# ----- Workspaces ------ #


@get.register
def get_all_workspaces(
    client: ClientV1,
    grai_type: WorkspaceLabels,
    options: ClientOptions = ClientOptions(),
) -> Optional[List[Workspace]]:
    resp = get(client, client.get_url(grai_type), options=options)
    resp = resp.json()

    if len(resp) == 0:
        return None
    else:
        return [Workspace(**item) for item in resp]


@get.register
def get_workspace_by_name_v1(
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
    resp = get(client, url, options=options)
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
            "{org-name}/{workspace-name} or the UUID of the desired workspace.",
        )

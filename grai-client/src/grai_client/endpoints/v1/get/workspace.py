from typing import List, Optional, Union
from uuid import UUID

from grai_schemas.v1 import WorkspaceV1
from grai_schemas.v1.workspace import WorkspaceSpec

from grai_client.endpoints.client import ClientOptions
from grai_client.endpoints.rest import get, get_is_unique, paginated_get
from grai_client.endpoints.utilities import (
    expects_unique_query,
    is_valid_uuid,
    paginated,
)
from grai_client.endpoints.v1.client import ClientV1
from grai_client.errors import ObjectNotFoundError
from grai_client.schemas.labels import WorkspaceLabels


@get.register
def get_all_workspaces(
    client: ClientV1,
    grai_type: WorkspaceLabels,
    options: ClientOptions = ClientOptions(),
) -> List[WorkspaceV1]:
    """

    Args:
        client:
        grai_type:
        options:  (Default value = ClientOptions())

    Returns:

    Raises:

    """
    resp = paginated_get(client, client.get_url(grai_type), options)
    return [WorkspaceV1.from_spec(item) for item in resp]


@get.register
def get_workspace_by_uuid(
    client: ClientV1,
    grai_type: WorkspaceLabels,
    workspace_id: Union[UUID, str],
    options: ClientOptions = ClientOptions(),
) -> Optional[WorkspaceV1]:
    """

    Args:
        client:
        grai_type:
        workspace_id:
        options:  (Default value = ClientOptions())

    Returns:

    Raises:

    """
    url = client.get_url(grai_type)
    if not is_valid_uuid(workspace_id):
        message = f"The provided workspace id {workspace_id} is not a valid uuid."
        raise ValueError(message)
    url = f"{url}{workspace_id}/"
    result = get(client, url, options=options)
    return WorkspaceV1.from_spec(result.json())


@get.register
def get_workspace_by_workspace_v1(
    client: ClientV1,
    grai_type: WorkspaceV1,
    options: ClientOptions = ClientOptions(),
) -> WorkspaceV1:
    """

    Args:
        client:
        grai_type:
        name:
        options:  (Default value = ClientOptions())

    Returns:

    Raises:

    """
    return get(client, grai_type.spec, options=options)


@get.register
def get_workspace_by_spec(
    client: ClientV1,
    grai_type: WorkspaceSpec,
    options: ClientOptions = ClientOptions(),
) -> WorkspaceV1:
    """

    Args:
        client:
        grai_type:
        name:
        options:  (Default value = ClientOptions())

    Returns:

    Raises:

    """
    if grai_type.id is not None:
        return get(client, "Workspace", grai_type.id, options=options)

    options = options.copy()
    options.query_args["ref"] = grai_type.ref
    resp = get_is_unique(client, "Workspace", options)

    return resp

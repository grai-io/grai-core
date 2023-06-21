from typing import Union

from grai_schemas.v1 import EdgeV1, NodeV1, SourceV1
from grai_schemas.v1.organization import OrganisationSpec, OrganisationV1
from grai_schemas.v1.workspace import WorkspaceSpec, WorkspaceV1

from grai_client.endpoints.client import ClientOptions
from grai_client.endpoints.rest import delete, get
from grai_client.endpoints.v1.client import ClientV1
from grai_client.errors import NotSupportedError
from grai_client.schemas.labels import (
    EdgeLabels,
    NodeLabels,
    OrganisationLabels,
    SourceEdgeLabels,
    SourceLabels,
    SourceNodeLabels,
    WorkspaceLabels,
)


@delete.register
def delete_node_v1(client: ClientV1, grai_type: NodeV1, options: ClientOptions = ClientOptions()):
    """

    Args:
        client:
        grai_type:
        options:  (Default value = ClientOptions())

    Returns:

    Raises:

    """
    if grai_type.spec.id is None:
        grai_type = get(client, grai_type)
        if grai_type is None:
            return
    url = f"{client.get_url(grai_type)}{grai_type.spec.id}/"
    delete(client, url, options=options)


@delete.register
def delete_edge_v1(client: ClientV1, grai_type: EdgeV1, options: ClientOptions = ClientOptions()):
    """

    Args:
        client:
        grai_type:
        options:  (Default value = ClientOptions())

    Returns:

    Raises:

    """
    if grai_type.spec.id is None:
        grai_type = get(client, grai_type)
        if grai_type is None:
            return
    url = f"{client.get_url(grai_type)}{grai_type.spec.id}/"
    delete(client, url, options=options)


@delete.register
def delete_workspace_v1(
    client: ClientV1,
    grai_type: Union[WorkspaceV1, WorkspaceSpec, WorkspaceLabels],
    options: ClientOptions = ClientOptions(),
):
    """

    Args:
        client:
        grai_type:
        options:  (Default value = ClientOptions())

    Returns:

    Raises:

    """
    message = (
        "The delete workspace endpoint is not supported through the REST API. If you wish to delete a workspace, "
        "please do so manually through the web application."
    )
    raise NotSupportedError(message)


@delete.register
def delete_organisation_v1(
    client: ClientV1,
    grai_type: Union[OrganisationV1, OrganisationSpec, OrganisationLabels],
    options: ClientOptions = ClientOptions(),
):
    """

    Args:
        client:
        grai_type:
        options:  (Default value = ClientOptions())

    Returns:

    Raises:

    """
    message = "The delete organisation endpoint is not supported through the REST API."
    raise NotSupportedError(message)


@delete.register
def delete_source_by_label(client: ClientV1, grai_type: SourceLabels, options: ClientOptions = ClientOptions()):
    """

    Args:
        client:
        grai_type:
        options:  (Default value = ClientOptions())

    Returns:

    Raises:

    """
    message = (
        "It's not possible to delete all sources through the REST API. If you really wish to delete all sources, "
        "You must do so iteratively through each individual source"
    )
    raise NotSupportedError(message)


@delete.register
def delete_source_by_source_v1(client: ClientV1, grai_type: SourceV1, options: ClientOptions = ClientOptions()):
    """

    Args:
        client:
        grai_type:
        options:  (Default value = ClientOptions())

    Returns:

    Raises:

    """
    if grai_type.spec.id is None:
        grai_type = get(client, grai_type)
        if grai_type is None:
            return
    url = f"{client.get_url(grai_type)}{grai_type.spec.id}/"
    delete(client, url, options=options)

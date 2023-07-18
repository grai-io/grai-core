from typing import Dict, Literal, Optional, Union
from uuid import UUID, uuid4

import httpx
from httpx import Response

from grai_client.endpoints.client import BaseClient, ClientOptions
from grai_client.endpoints.rest import delete, get, patch, post
from grai_client.endpoints.utilities import (
    add_query_params,
    is_valid_uuid,
    response_status_check,
    serialize_obj,
)


class ClientV1(BaseClient):
    """ """

    id: Literal["v1"] = "v1"
    base = "/api/v1/"
    _node_endpoint = "lineage/nodes/"
    _edge_endpoint = "lineage/edges/"
    _source_endpoint = "lineage/sources/"
    _workspace_endpoint = "workspaces/"
    _is_authenticated_endpoint = "auth/is-authenticated/"

    def __init__(self, *args, workspace: Optional[Union[str, UUID]] = None, **kwargs):
        super().__init__(*args, **kwargs)
        self.api = f"{self.url}{self.base}"
        self.node_endpoint = f"{self.api}{self._node_endpoint}"
        self.edge_endpoint = f"{self.api}{self._edge_endpoint}"
        self.source_endpoint = f"{self.api}{self._source_endpoint}"
        self.workspace_endpoint = f"{self.api}{self._workspace_endpoint}"
        self.is_authenticated_endpoint = f"{self.api}{self._is_authenticated_endpoint}"

        self._workspace = None
        self.workspace_label = str(workspace)

        if self.init_auth_values.is_valid():
            self.authenticate(**self.init_auth_values.dict())

    def check_authentication(self) -> Response:
        """

        Args:

        Returns:

        Raises:

        """
        return httpx.get(self.is_authenticated_endpoint, auth=self.auth)

    @property
    def workspace(self) -> Optional[str]:
        """

        Args:

        Returns:

        Raises:

        """
        return self._workspace

    @workspace.setter
    def workspace(self, workspace: Optional[Union[str, UUID]]):
        """

        Args:
            workspace (Optional[Union[str, UUID]]):

        Returns:

        Raises:

        """
        if workspace is None:
            self._workspace = workspace
            self.workspace_label = workspace
            self.default_query_args.pop("workspace", None)
            return

        elif is_valid_uuid(workspace):
            result = self.get("workspace", workspace).spec
            if result is None:
                raise ValueError(f"No workspace found matching `{workspace}`")
        elif isinstance(workspace, str):
            has_ref = False
            if "/" in workspace:  # workspace ref
                result = self.get("workspace", ref=workspace)
                has_ref = True
            else:  # workspace name
                result = self.get("workspace", name=workspace)

            if (num_results := len(result)) == 0:
                raise ValueError(f"No workspace found matching `{workspace}`")
            elif num_results > 1:
                raise ValueError(
                    f"Multiple workspaces found matching `{workspace}`"
                    f"If you've specified a workspace name and belong to multiple organizations, please use the ref "
                    "which looks like `{organization}/{workspace}` instead of the name to disambiguate."
                )
            elif (result[0].spec.ref if has_ref else result[0].spec.name) != workspace:
                message = (
                    f"Although you specified workspace `{workspace}` in the client. We could not identify a "
                    f"corresponding workspace for the authenticated user in the server. The associated workspace we "
                    f"identified for the user was {result[0].spec.ref}"
                )
                raise Exception(message)

            workspace = result[0].spec.id
        else:
            raise TypeError("Workspace must be either a string, uuid, or None.")

        self._workspace = str(workspace)
        self.workspace_label = self._workspace
        self.default_query_args["workspace"] = self._workspace

    def authenticate(
        self,
        username: Optional[str] = None,
        password: Optional[str] = None,
        api_key: Optional[str] = None,
    ) -> None:
        """

        Args:
            username (Optional[str], optional):  (Default value = None)
            password (Optional[str], optional):  (Default value = None)
            api_key (Optional[str], optional):  (Default value = None)

        Returns:

        Raises:

        """
        super().authenticate(username, password, api_key)
        self.workspace = self.workspace_label


@patch.register
def client_patch_url(
    client: ClientV1,
    url: str,
    payload: Dict,
    options: ClientOptions = ClientOptions(),
) -> Response:
    """

    Args:
        client (BaseClient):
        url (str):
        payload (Dict):
        options (ClientOptions, optional):  (Default value = ClientOptions())

    Returns:

    Raises:

    """
    headers = {"Content-Type": "application/json", **options.headers}
    payload = {**payload, **options.payload}

    query_args = {"workspace": client.workspace, **options.query_args}
    url = add_query_params(url, query_args)

    response = client.session.patch(url, content=serialize_obj(payload), headers=headers, **options.request_args)

    response_status_check(response)
    return response


@post.register
def client_post_url(
    client: ClientV1,
    url: str,
    payload: Dict,
    options: ClientOptions = ClientOptions(),
) -> Response:
    """

    Args:
        client (BaseClient):
        url (str):
        payload (Dict):
        options (ClientOptions, optional):  (Default value = ClientOptions())

    Returns:

    Raises:

    """
    headers = {"Content-Type": "application/json", **options.headers}
    payload = {**payload, **options.payload}

    query_args = {"workspace": client.workspace, **options.query_args}
    url = add_query_params(url, query_args)
    response = client.session.post(url, content=serialize_obj(payload), headers=headers, **options.request_args)

    response_status_check(response)
    return response


@delete.register
def client_delete_url(client: ClientV1, url: str, options: ClientOptions = ClientOptions()) -> Response:
    """

    Args:
        client (BaseClient):
        url (str):
        options (ClientOptions, optional):  (Default value = ClientOptions())

    Returns:

    Raises:

    """
    query_args = {"workspace": client.workspace, **options.query_args}
    url = add_query_params(url, query_args)

    response = client.session.delete(url, headers=options.headers, **options.request_args)
    response_status_check(response)
    return response


@get.register
def client_get_url(client: ClientV1, url: str, options: ClientOptions = ClientOptions()) -> Response:
    """

    Args:
        client (BaseClient):
        url (str):
        options (ClientOptions, optional):  (Default value = ClientOptions())

    Returns:

    Raises:

    """

    query_args = {"workspace": client.workspace, **options.query_args}
    url = add_query_params(url, query_args)

    response = client.session.get(url, headers=options.headers, **options.request_args)
    response_status_check(response)
    return response

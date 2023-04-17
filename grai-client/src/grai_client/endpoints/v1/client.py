import asyncio
from typing import Optional, Union
from uuid import UUID, uuid4

from httpx import Response

from grai_client.endpoints.client import BaseClient
from grai_client.endpoints.utilities import is_valid_uuid


class ClientV1(BaseClient):
    id = "v1"
    base = "/api/v1/"
    _node_endpoint = "lineage/nodes/"
    _edge_endpoint = "lineage/edges/"
    _workspace_endpoint = "workspaces/"
    _is_authenticated_endpoint = "auth/is-authenticated/"

    def __init__(self, *args, workspace: Optional[Union[str, UUID]] = None, **kwargs):
        super().__init__(*args, **kwargs)
        self.api = f"{self.url}{self.base}"
        self.node_endpoint = f"{self.api}{self._node_endpoint}"
        self.edge_endpoint = f"{self.api}{self._edge_endpoint}"
        self.workspace_endpoint = f"{self.api}{self._workspace_endpoint}"
        self.is_authenticated_endpoint = f"{self.api}{self._is_authenticated_endpoint}"

        self._workspace = str(workspace) if workspace is not None else None

    def check_authentication(self) -> Response:
        return asyncio.run(self.session.get(self.is_authenticated_endpoint, headers=self.auth_headers))

    @property
    def workspace(self) -> Optional[str]:
        return self._workspace

    @workspace.setter
    def workspace(self, workspace: Optional[Union[str, UUID]]):
        if workspace is None:
            self._workspace = workspace
            self.default_payload.pop("workspace", None)
            return

        if is_valid_uuid(workspace):
            pass
        elif isinstance(workspace, str):
            result = self.get("workspace", workspace)

            if result is None:
                raise Exception(f"No workspace matching `name={workspace}`")
            else:
                workspace = result.id
        else:
            raise TypeError("Workspace must be either a string, uuid, or None.")

        self._workspace = str(workspace)
        self.default_payload["workspace"] = self._workspace

    def authenticate(
        self,
        username: Optional[str] = None,
        password: Optional[str] = None,
        api_key: Optional[str] = None,
    ) -> None:
        super().authenticate(username, password, api_key)
        self.workspace = self.workspace

    def set_authentication_headers(
        self,
        username: Optional[str] = None,
        password: Optional[str] = None,
        api_key: Optional[str] = None,
    ) -> None:
        # Deprecated
        self.authenticate(username, password, api_key)

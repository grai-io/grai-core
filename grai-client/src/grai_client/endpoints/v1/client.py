from typing import Optional, Union
from uuid import UUID, uuid4

import requests

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

        self._workspace = workspace

    def check_authentication(self) -> requests.Response:
        result = requests.get(self.is_authenticated_endpoint, headers=self.auth_headers)
        return result

    @property
    def workspace(self) -> str:
        return self._workspace

    @workspace.setter
    def workspace(self, workspace: Optional[Union[str, UUID]]):
        if workspace is None:
            self._workspace = workspace
            self.default_payload.pop("workspace", None)
            return

        if isinstance(workspace, UUID):
            workspace = str(workspace)
        elif isinstance(workspace, str):
            if not is_valid_uuid(workspace):
                result = self.get("workspace", workspace)

                if result is None:
                    raise Exception(f"No workspace matching `name={workspace}`")
                else:
                    workspace = str(result.id)
        else:
            raise TypeError("Workspace must be either a string, uuid, or None.")

        self._workspace = workspace
        self.default_payload["workspace"] = self._workspace

    def set_authentication_headers(self, *args, **kwargs):
        super().set_authentication_headers(*args, **kwargs)
        self.workspace = self.workspace

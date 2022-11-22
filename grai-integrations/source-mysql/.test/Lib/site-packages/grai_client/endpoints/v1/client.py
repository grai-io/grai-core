import requests
from grai_client.endpoints.client import BaseClient
from grai_client.endpoints.utilities import (GraiEncoder,
                                             response_status_check)

class ClientV1(BaseClient):
    id = "v1"
    base = "/api/v1/"
    _node_endpoint = "lineage/nodes/"
    _edge_endpoint = "lineage/edges/"
    _is_authenticated = "auth/is-authenticated/"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.api = f"{self.url}{self.base}"
        self.node_endpoint = f"{self.api}{self._node_endpoint}"
        self.edge_endpoint = f"{self.api}{self._edge_endpoint}"
        self.is_authenticated_endpoint = f"{self.api}{self._is_authenticated}"

    def check_authentication(self) -> requests.Response:
        result = requests.get(self.is_authenticated_endpoint, headers=self.auth_headers)
        return result


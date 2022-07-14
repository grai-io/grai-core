from grai_cli.server.endpoints.client import BaseClient
from functools import singledispatchmethod, singledispatch
from typing import Any, Type, Dict
import requests
from grai_cli.server.utilities import response_auth_checker


class ClientV1(BaseClient):
    id = 'v1'
    base = '/api/v1/'
    _node_endpoint = 'lineage/nodes/'
    _edge_endpoint = 'lineage/edges/'
    _is_authenticated = 'auth/is-authenticated/'

    def __init__(self):
        super().__init__()
        self.api = f"{self.url}{self.base}"
        self.node_endpoint = f"{self.api}{self._node_endpoint}"
        self.edge_endpoint = f"{self.api}{self._edge_endpoint}"
        self.is_authenticated_endpoint = f"{self.api}{self._edge_endpoint}"

    def check_authentication(self) -> requests.Response:
        result = requests.get(self.is_authenticated_endpoint, headers=self.authentication_headers())
        return result

    @singledispatchmethod
    def get(self, grai_type: Any) -> Dict:
        raise NotImplementedError(f"No get method implemented for type {type(grai_type)}")

    @singledispatchmethod
    def post(self, grai_type: Any) -> Dict:
        raise NotImplementedError(f"No get method implemented for type {type(grai_type)}")
import abc
from functools import singledispatch, singledispatchmethod
from typing import Any, Dict, Union, Optional

from grai_client.authentication import (APIKeyHeader, UserNameHeader,
                                        UserTokenHeader)
from multimethod import multimethod


class BaseClient:
    id = "base"

    def __init__(self, host: str, port: str):
        self.host = host
        self.port = port
        self.url = f"http://{self.host}:{self.port}"
        self.api = f"{self.url}"
        self._auth_headers = None

    def build_url(self, endpoint: str) -> str:
        return f"{self.api}{endpoint}"

    @property
    def auth_headers(self) -> Dict:
        if not self._auth_headers:
            raise Exception(
                "Client not authenticated. Please call `set_authentication_headers` with your credentials first"
            )
        return self._auth_headers

    def set_authentication_headers(
        self,
        username: Optional[str] = None,
        password: Optional[str] = None,
        token: Optional[str] = None,
        api_key: Optional[str] = None,
    ):
        if username and password:
            self._auth_headers = UserNameHeader(username, password).headers
        elif token:
            self._auth_headers = UserTokenHeader(token).headers
        elif api_key:
            self._auth_headers = APIKeyHeader(api_key).headers
        else:
            raise Exception(
                "Authentication requires either a user token, api key, or username/password combo."
            )

    def check_authentication(self):
        raise NotImplementedError(f"No authentication implemented for {type(self)}")

    @multimethod
    def get(self, grai_type: Any) -> Dict:
        raise NotImplementedError(
            f"No get method implemented for type {type(grai_type)}"
        )

    @multimethod
    def post(self, grai_type: Any) -> Dict:
        raise NotImplementedError(
            f"No post method implemented for type {type(grai_type)}"
        )

    @multimethod
    def patch(self, grai_type: Any) -> Dict:
        raise NotImplementedError(
            f"No patch method implemented for type {type(grai_type)}"
        )

    @multimethod
    def delete(self, grai_type: Any) -> Dict:
        raise NotImplementedError(
            f"No delete method implemented for type {type(grai_type)}"
        )

import abc
from typing import Any, Dict, Union, Optional, List, Sequence
from grai_client.schemas.schema import GraiType
from grai_client.authentication import (APIKeyHeader, UserNameHeader,
                                        UserTokenHeader)
from grai_client.endpoints.utilities import response_status_check, GraiEncoder
from multimethod import multimethod

import requests
import json


class BaseClient(abc.ABC):
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
    def get_url(self, grai_type: Any) -> str:
        raise NotImplementedError(
            f"No url method implemented for type {type(grai_type)}"
        )

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

@BaseClient.post.register
def post_sequence(client: BaseClient, objs: Sequence) -> List[Dict]:
    result = [client.post(obj) for obj in objs]
    return result


@BaseClient.patch.register
def patch_sequence(client: BaseClient, objs: Sequence) -> List[Dict]:
    result = [client.patch(obj) for obj in objs]
    return result


@BaseClient.delete.register
def delete_sequence(client: BaseClient, objs: Sequence[GraiType]):
    for obj in objs:
        client.delete(obj)


@BaseClient.get.register
def get_sequence(client: BaseClient, objs: Sequence) -> List[Dict]:
    result = [client.get(obj) for obj in objs]
    return result


@BaseClient.get.register
def get_url_v1(client: BaseClient, url: str) -> requests.Response:
    response = requests.get(url, headers=client.auth_headers)
    response_status_check(response)
    return response


@BaseClient.delete.register
def delete_url_v1(client: BaseClient, url: str) -> requests.Response:
    response = requests.delete(url, headers=client.auth_headers)
    response_status_check(response)
    return response


@BaseClient.patch.register
def patch_url_v1(client: BaseClient, url: str, payload: Dict) -> requests.Response:
    headers = {**client.auth_headers, "Content-Type": "application/json"}
    payload = {k: v for k, v in payload.items() if v is not None}
    response = requests.patch(
        url, data=json.dumps(payload, cls=GraiEncoder), headers=headers
    )

    response_status_check(response)
    return response


@BaseClient.post.register
def post_url_v1(client: BaseClient, url: str, payload: Dict) -> requests.Response:
    headers = {**client.auth_headers, "Content-Type": "application/json"}
    payload = {k: v for k, v in payload.items() if v is not None}
    response = requests.post(url, data=json.dumps(payload, cls=GraiEncoder), headers=headers)
    response_status_check(response)
    return response
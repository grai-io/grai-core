import abc
import json
from functools import wraps
from typing import (
    Any,
    Callable,
    Concatenate,
    Dict,
    List,
    Optional,
    ParamSpec,
    Sequence,
    Tuple,
    Union,
    TypeVar,
)

import requests
from grai_client.authentication import APIKeyHeader, UserNameHeader, UserTokenHeader
from grai_client.endpoints.utilities import response_status_check, serialize_obj
from grai_client.schemas.schema import GraiType
from multimethod import multimethod
from pydantic import BaseModel
from typing_extensions import TypeVarTuple, Unpack

R = TypeVar("R")
T = TypeVar("T")
Ts = TypeVarTuple("Ts")


class ClientOptions(BaseModel):
    payload: Dict = {}
    request_args: Dict = {}
    headers: Dict = {}


func_type = Callable[[T, Unpack[Ts], Optional[ClientOptions]], R]

OptionType = Optional[Union[Dict, ClientOptions]]


def unwrap_options(func: Callable[[T, Unpack[Ts]], R]) -> func_type:
    @wraps(func)
    def inner(self, *args, options=ClientOptions(), **kwargs) -> R:
        if isinstance(options, ClientOptions):
            pass
        elif isinstance(options, Dict):
            options = ClientOptions(**options)
        else:
            raise NotImplementedError(f"Unrecognized options type: {type(options)}")
        return func(self, *args, options=options, **kwargs)

    return inner


@multimethod
def get(*args, **kwargs) -> None:
    pass


@get.register()
def get_default(*args) -> None:
    raise NotImplementedError(
        f"No get method implemented for type {[type(arg) for arg in args]}"
    )


@multimethod
def post(*args, **kwargs) -> None:
    pass


@post.register()
def post_default(*args, **kwargs) -> None:
    raise NotImplementedError(
        f"No post method implemented for type {[type(arg) for arg in args]}"
    )


@multimethod
def patch(*args, **kwargs) -> None:
    pass


@patch.register()
def patch_default(*args, **kwargs) -> None:
    raise NotImplementedError(
        f"No patch method implemented for type {[type(arg) for arg in args]}"
    )


@multimethod
def delete(*args, **kwargs) -> None:
    pass


@delete.register()
def delete_default(*args, **kwargs) -> None:
    raise NotImplementedError(
        f"No delete method implemented for types {[type(arg) for arg in args]}"
    )


class BaseClient(abc.ABC):
    id = "base"

    def __init__(self, host: str, port: str):
        self.host = host
        self.port = port

        prefix = "https" if self.port == "443" else "http"
        self.url = f"{prefix}://{self.host}:{self.port}"
        self.api = f"{self.url}"
        self._auth_headers = None

        if not self.check_server_status():
            raise Exception(f"Server at {self.url} is not responding.")

    def check_server_status(self) -> bool:
        resp = requests.get(f"{self.url}/health/")
        return resp.status_code == 200

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
    ) -> None:
        if username and password:
            self._auth_headers = UserNameHeader(username, password, self.url).headers
        elif token:
            self._auth_headers = UserTokenHeader(token).headers
        elif api_key:
            self._auth_headers = APIKeyHeader(api_key).headers
        else:
            raise Exception(
                "Authentication requires either a user token, api key, or username/password combo."
            )

    def check_authentication(self) -> requests.Response:
        raise NotImplementedError(f"No authentication implemented for {type(self)}")

    @multimethod
    def get_url(self, grai_type: Any) -> str:
        raise NotImplementedError(
            f"No url method implemented for type {type(grai_type)}"
        )

    @unwrap_options
    def get(self, *args, options=ClientOptions(), **kwargs):
        return get(self, *args, options=options)

    @unwrap_options
    def post(self, *args, options=ClientOptions(), **kwargs):
        return post(self, *args, options=options)

    @unwrap_options
    def patch(self, *args, options=ClientOptions(), **kwargs):
        return patch(self, *args, options=options)

    @unwrap_options
    def delete(self, *args, options=ClientOptions(), **kwargs) -> Dict:
        return delete(self, *args, options=options)


@get.register
def get_sequence(
    client: BaseClient, objs: Sequence, options: ClientOptions = ClientOptions()
) -> List[Dict]:
    result = [client.get(obj, options=options) for obj in objs]
    return result


@delete.register
def delete_sequence(
    client: BaseClient, objs: Sequence, options: ClientOptions = ClientOptions()
) -> None:
    for obj in objs:
        client.delete(obj, options=options)


@post.register
def post_sequence(
    client: BaseClient, objs: Sequence, options: ClientOptions = ClientOptions()
) -> List[Dict]:
    result = [client.post(obj, options=options) for obj in objs]
    return result


@patch.register
def patch_sequence(
    client: BaseClient, objs: Sequence, options: ClientOptions = ClientOptions()
) -> List[Dict]:
    result = [client.patch(obj, options=options) for obj in objs]
    return result


#  -------------------------------  #


@get.register
def get_url_v1(
    client: BaseClient, url: str, options: ClientOptions = ClientOptions()
) -> requests.Response:
    headers = {**client.auth_headers, **options.headers}

    response = requests.get(url, headers=headers, **options.request_args)
    response_status_check(response)
    return response


@delete.register
def delete_url_v1(
    client: BaseClient, url: str, options: ClientOptions = ClientOptions()
) -> requests.Response:
    headers = {**client.auth_headers, **options.headers}

    response = requests.delete(url, headers=headers, **options.request_args)
    response_status_check(response)
    return response


@post.register
def post_url_v1(
    client: BaseClient,
    url: str,
    payload: Dict,
    options: ClientOptions = ClientOptions(),
) -> requests.Response:
    headers = client.auth_headers
    headers = {**client.auth_headers, "Content-Type": "application/json", **options.headers}
    payload = {**payload, **options.payload}
    print(headers)
    response = requests.post(
        url, data=serialize_obj(payload), headers=headers#, **options.request_args
    )

    response_status_check(response)
    return response


@patch.register
def patch_url_v1(
    client: BaseClient,
    url: str,
    payload: Dict,
    options: ClientOptions = ClientOptions(),
) -> requests.Response:
    headers = {**client.auth_headers, "Content-Type": "application/json", **options.headers}
    payload = {**payload, **options.payload}

    response = requests.patch(
        url, data=serialize_obj(payload), headers=headers, **options.request_args
    )

    response_status_check(response)
    return response

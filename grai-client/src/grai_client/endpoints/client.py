import abc
import json
import sys
import warnings
from functools import wraps
from typing import (
    Any,
    Callable,
    Coroutine,
    Dict,
    Iterable,
    List,
    Literal,
    Optional,
    Sequence,
    Tuple,
    Type,
    TypeVar,
    Union,
)
from urllib.parse import urlparse

import httpx
from grai_schemas.base import Edge, Node
from httpx import Auth, BasicAuth, QueryParams, Request, Response
from multimethod import multimethod
from pydantic import BaseModel, SecretStr
from tqdm.autonotebook import tqdm

from grai_client.authentication import APIKeyAuth
from grai_client.endpoints.rest import delete, get, patch, post
from grai_client.endpoints.utilities import (
    add_query_params,
    response_status_check,
    serialize_obj,
)
from grai_client.schemas.schema import GraiType

if sys.version_info < (3, 10):
    from typing_extensions import ParamSpec
else:
    from typing import ParamSpec

P = ParamSpec("P")
R = TypeVar("R", covariant=True)
T = TypeVar("T")
OptionType = Union[Dict, "ClientOptions"]
ResultTypes = Union[Optional[GraiType], Sequence[Optional[GraiType]]]
SegmentedCallerType = Callable[["BaseClient", Sequence, "ClientOptions"], List[T]]
ProtocolType = Union[Literal["http"], Literal["https"]]


class ClientOptions(BaseModel):
    payload: Dict = {}
    request_args: Dict = {}
    headers: Dict = {}
    query_args: Dict = {}

    @classmethod
    def __hash__(cls):
        return id(cls)

    def __add__(self, other: Union[Dict, "ClientOptions"]) -> "ClientOptions":
        if isinstance(other, Dict):
            other = ClientOptions(**other)
        elif not isinstance(other, ClientOptions):
            raise NotImplementedError(f"Unrecognized options type: {type(other)}")

        payload = {**self.payload, **other.payload}
        request_args = {**self.request_args, **other.request_args}
        headers = {**self.headers, **other.headers}
        query_args = {**self.query_args, **other.query_args}
        return ClientOptions(payload=payload, request_args=request_args, headers=headers, query_args=query_args)


def validate_connection_arguments(
    url: Optional[str] = None,
    host: Optional[str] = None,
    port: Optional[str] = None,
    protocol: Optional[ProtocolType] = None,
    insecure: Optional[bool] = None,
) -> Tuple[str, str, Optional[str], ProtocolType, bool]:
    if url is not None:
        # derive from url
        parsed_url = urlparse(url)
        url_protocol = parsed_url.scheme
        url_host = parsed_url.hostname
        url_port = str(parsed_url.port) if parsed_url.port is not None else None
        url_insecure = True if url_protocol == "http" else False

        if protocol is not None and url_protocol != protocol:
            message = (
                f"The provided url `{url}` uses the protocol {url_protocol}, but you've specified `protocol={protocol}`."
                f" Because these values differ we've defaulted to the protocol specified in the url"
            )
            warnings.warn(message)
        if host is not None and url_host != host:
            message = (
                f"The provided url `{url}` uses the host {url_host}, but you've specified `host={host}`."
                f" Because these values differ we've defaulted to the host specified in the url"
            )
            warnings.warn(message)
        if port is not None and url_port != port:
            message = (
                f"The provided url `{url}` uses the port {url_port} (which may come from it's protocol), but you've "
                f"specified `port={port}`. Because these values differ we've defaulted to the port "
                f"specified in the url"
            )
            warnings.warn(message)
        if insecure is not None and url_insecure != insecure:
            message = (
                f"The provided url `{url}` uses {'an insecure' if url_insecure else 'a secure'} connection, but you've "
                f"specified `insecure={insecure}`. Because these values differ we've defaulted to the security level "
                f"specified in the url."
            )
            warnings.warn(message)

        protocol = url_protocol
        host = url_host
        port = url_port
        insecure = url_insecure
    else:
        assert host, f"Client connections require at minimum a value for `url` or `host`."
        if port is None and host == "localhost":
            port = "8000"

        if protocol is None:
            protocol = "http" if insecure is True else "https"
            insecure = False if insecure is None else insecure
        else:
            # Protocol value was provided by the user
            if insecure is None:
                insecure = True if protocol == "http" else False
            else:
                # Both protocol and insecure values were provided by the user. Secure connections win.
                if not isinstance(insecure, bool):
                    message = f"Unexpected `insecure` value: {insecure}, `insecure` must be either True or False."
                    raise ValueError(message)
                if insecure is False and protocol == "http":
                    message = (
                        "By setting `insecure=False` you've requested a secure connection. However, it's "
                        "not possible to establish a secure connection using the http protocol. As a result "
                        "we've defaulted the protocol to https. To remove this warning either set "
                        "`insecure=True` or `protocol='https'`."
                    )
                    warnings.warn(message)
                    protocol = "https"
                elif insecure is True and protocol == "https":
                    message = (
                        "By setting `insecure=True` you've requested an insecure connection. However, it's not "
                        "possible to establish an insecure connection using the https protocol which is secure "
                        "by default. In order to protect your data we've defaulted to `insecure=False`. "
                        "To remove this warning either set `insecure=False` or `protocol='http'`."
                    )
                    warnings.warn(message)
                    insecure = False

        url = f"{protocol}://{host}"
        if port is not None:
            try:
                int(port)
            except:
                raise ValueError(f"Expected a valid integer value for `port` not {port}")
            url = f"{url}:{port}"

    if protocol not in ("http", "https", None):
        message = f"Unexpected `protocol` value: {protocol}, `protocol` must be one of 'http' or 'https'."
        raise ValueError(message)

    return url, host, port, protocol, insecure


class AuthValues(BaseModel):
    username: Optional[str] = None
    password: Optional[SecretStr] = None
    api_key: Optional[SecretStr] = None

    def is_valid(self) -> bool:
        return self.api_key is not None or (self.username is not None and self.password is not None)

    def get_auth(self) -> Auth:
        if self.api_key is not None:
            auth = APIKeyAuth(self.api_key.get_secret_value())
        elif self.username is not None and self.password is not None:
            auth = BasicAuth(self.username, self.password.get_secret_value())
        else:
            message = "Auth requires either a not null value for api_key, or username and password."
            raise Exception(message)
        return auth


def async_requires_auth(func):
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        if self.is_authenticated:
            return func(self, *args, **kwargs)
        else:
            raise Exception("This method requires authentication. Call `authenticate` first.")

    return wrapper


def requires_auth(func):
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        if self.is_authenticated:
            return func(self, *args, **kwargs)
        else:
            raise Exception("This method requires authentication. Call `authenticate` first.")

    return wrapper


class BaseClient(abc.ABC):
    id = "base"
    api: str
    health_endpoint: str
    node_endpoint: str
    edge_endpoint: str
    workspace_endpoint: str
    is_authenticated_endpoint: str

    def __init__(
        self,
        host: Optional[str] = None,
        port: Optional[str] = None,
        protocol: Optional[ProtocolType] = None,
        insecure: Optional[bool] = None,
        url: Optional[str] = None,
        httpx_client_args: Optional[Union[Dict[str, Any], str]] = None,
        username: Optional[str] = None,
        password: Optional[str] = None,
        api_key: Optional[str] = None,
    ):
        # TODO: Should require keyword arguments
        validated_args = validate_connection_arguments(url, host, port, protocol, insecure)
        if isinstance(httpx_client_args, str):
            httpx_client_args = json.loads(httpx_client_args)

        self.url: str = validated_args[0]
        self.host: str = validated_args[1]
        self.port: Optional[str] = validated_args[2]
        self.protocol: ProtocolType = validated_args[3]
        self.insecure: bool = validated_args[4]
        self.httpx_client_args: Dict[str, Any] = httpx_client_args

        self.health_endpoint: str = f"{self.url}/health"

        self.is_authenticated: bool = False
        self.init_auth_values: AuthValues = AuthValues(username=username, password=password, api_key=api_key)
        self._auth: Optional[Auth] = None

        self.default_payload: Dict[str, str] = dict()
        self.default_headers: Dict[str, str] = dict()
        self.default_request_args: Dict[str, str] = dict()
        self.default_query_args: Dict[str, str] = dict()

        self.session: Optional[httpx.Client] = None

        if (resp := self.server_health_status()).status_code != 200:
            raise Exception(f"Error connecting to server at {self.url}. Received response {resp.json()}")

    def get_session(self) -> httpx.Client:
        client_args = {"timeout": None, "http2": True, "params": QueryParams(**self.default_query_args)}
        client_args.update(self.httpx_client_args if self.httpx_client_args is not None else {})

        session = httpx.Client(**client_args)
        session.auth = self.auth
        return session

    @property
    def default_options(self) -> ClientOptions:
        return ClientOptions(
            **{
                "payload": self.default_payload,
                "headers": self.default_headers,
                "request_args": self.default_request_args,
                "query_args": self.default_query_args,
            }
        )

    def server_health_status(self) -> Response:
        return httpx.get(self.health_endpoint)

    @property
    def auth(self) -> Auth:
        if self._auth is None:
            # if self._init_auth_values.is_valid():
            #     self.auth = self._init_auth_values.get_auth()
            # else:
            raise Exception("Client not authenticated. Please call `authenticate` with your credentials first")
        return self._auth

    @auth.setter
    def auth(self, auth: Auth) -> None:
        old_auth = self._auth
        if not isinstance(auth, Auth):
            raise TypeError(f"Expected an instance of `httpx.Auth` not {type(auth)}")
        self._auth = auth

        try:
            resp = self.check_authentication()
        except Exception as e:
            self._auth = old_auth
            raise e

        if resp.status_code != 200:
            message = (
                f"Unable to authenticate connection to the server with the provided credentials. ",
                f"Received status_code: {resp.status_code}",
            )
            self._auth = old_auth
            raise Exception(message)

        self.is_authenticated = True

    def authenticate(
        self,
        username: Optional[str] = None,
        password: Optional[str] = None,
        api_key: Optional[str] = None,
    ) -> None:
        auth_values = AuthValues(username=username, password=password, api_key=api_key)
        self.auth = auth_values.get_auth()

    @abc.abstractmethod
    def check_authentication(self) -> Response:
        raise NotImplementedError(f"No authentication implemented for {type(self)}")

    @multimethod
    def get_url(self, grai_type: Any) -> str:
        raise NotImplementedError(f"No url method implemented for type {type(grai_type)}")

    def session_manager(self, func: Callable, *args, options: Optional[OptionType] = None, **kwargs):
        if options is None:
            options = ClientOptions()

        options = self.default_options + options
        options.query_args = {**options.query_args, **kwargs}

        with self.get_session() as session:
            self.session = session
            result = func(self, *args, options=options)
        self.session = None
        return result

    @requires_auth
    def get(self, *args, options: Optional[OptionType] = None, **kwargs):
        return self.session_manager(get, *args, options=options, **kwargs)

    @requires_auth
    def post(self, *args, options: Optional[OptionType] = None, **kwargs):
        return self.session_manager(post, *args, options=options, **kwargs)

    @requires_auth
    def patch(self, *args, options: Optional[OptionType] = None, **kwargs):
        return self.session_manager(patch, *args, options=options, **kwargs)

    @requires_auth
    def delete(self, *args, options: Optional[OptionType] = None, **kwargs):
        return self.session_manager(delete, *args, options=options, **kwargs)


# ----- Sequence Functions ----- #


def type_segmentation(
    objs: Sequence, priority_order: Optional[Tuple[Type[T]]]
) -> List[Tuple[List[int], Union[Sequence[T], Iterable[T]], Type[T]]]:
    if priority_order is None:
        return [(list(range(len(objs))), objs, Any)]

    obj_idx_map: Dict[Type[T], List[int]] = {}
    for idx, obj in enumerate(objs):
        obj_type: Type[T] = type(obj)
        obj_idx_map.setdefault(obj_type, [])
        obj_idx_map[obj_type].append(idx)

    result_iter: List[Tuple[List[int], Iterable[T], Type[T]]] = []
    for prioritized_type in priority_order:
        type_keys = [obj_type for obj_type in obj_idx_map.keys() if issubclass(obj_type, prioritized_type)]
        for obj_type in type_keys:
            idx = obj_idx_map.pop(obj_type)
            result_iter.append((idx, (objs[i] for i in idx), obj_type))

    for obj_type, idx in obj_idx_map.items():
        result_iter.append((idx, (objs[i] for i in idx), obj_type))

    return result_iter


PRIORITY_ORDER_MAP = {
    "post": (Node, Edge),
    "delete": (Edge, Node),
    "patch": None,
    "get": None,
}


def segmented_caller(
    func: Callable[[BaseClient, Sequence[T], ClientOptions], R], priority_order: Optional[Tuple] = None
) -> Callable[[BaseClient, Sequence[T], ClientOptions], list[R]]:
    if priority_order is None:
        priority_order = PRIORITY_ORDER_MAP.get(func.__name__, ())

    def inner(client: BaseClient, objs: Sequence[T], options: ClientOptions) -> List[R]:
        final_result = [None] * len(objs)
        pbar = tqdm(
            type_segmentation(objs, priority_order),
            desc=func.__name__.capitalize(),
            # colour='#ffb567',
            position=0,
        )
        for index, iter_obj, obj_type in pbar:
            inner_pbar = tqdm(
                iter_obj,
                desc=obj_type.__name__,
                unit=f" {obj_type.__name__}",
                # colour='#8338ec',
                position=1,
                leave=True,
            )
            result = [func(client, obj, options) for obj in inner_pbar]

            for i, obj in zip(index, result):
                final_result[i] = obj
        return final_result

    return inner


@get.register
def get_sequence(
    client: BaseClient,
    objs: Sequence,
    options: ClientOptions = ClientOptions(),
) -> Sequence[T]:
    segmented_get = segmented_caller(get)
    result = segmented_get(client, objs, options)
    return result


@delete.register
def delete_sequence(
    client: BaseClient,
    objs: Sequence,
    options: ClientOptions = ClientOptions(),
) -> None:
    segmented_delete = segmented_caller(delete)
    result = segmented_delete(client, objs, options)
    return None


@post.register
def post_sequence(
    client: BaseClient,
    objs: Sequence,
    options: ClientOptions = ClientOptions(),
) -> List[T]:
    segmented_post = segmented_caller(post)
    result = segmented_post(client, objs, options)
    return result


@patch.register
def patch_sequence(
    client: BaseClient,
    objs: Sequence,
    options: ClientOptions = ClientOptions(),
) -> List[T]:
    segmented_patch = segmented_caller(patch)
    result = segmented_patch(client, objs, options)
    return result


# -------------------------------------------- #


@get.register
def client_get_url(client: BaseClient, url: str, options: ClientOptions = ClientOptions()) -> Response:
    if options.query_args:
        url = add_query_params(url, options.query_args)
    response = client.session.get(url, headers=options.headers, **options.request_args)
    response_status_check(response)
    return response


@delete.register
def client_delete_url(client: BaseClient, url: str, options: ClientOptions = ClientOptions()) -> Response:
    response = client.session.delete(url, headers=options.headers, **options.request_args)
    response_status_check(response)
    return response


@post.register
def client_post_url(
    client: BaseClient,
    url: str,
    payload: Dict,
    options: ClientOptions = ClientOptions(),
) -> Response:
    headers = {
        "Content-Type": "application/json",
        **options.headers,
    }
    payload = {**payload, **options.payload}

    response = client.session.post(url, content=serialize_obj(payload), headers=headers, **options.request_args)

    response_status_check(response)
    return response


@patch.register
def client_patch_url(
    client: BaseClient,
    url: str,
    payload: Dict,
    options: ClientOptions = ClientOptions(),
) -> Response:
    headers = {
        "Content-Type": "application/json",
        **options.headers,
    }
    payload = {**payload, **options.payload}

    response = client.session.patch(url, content=serialize_obj(payload), headers=headers, **options.request_args)

    response_status_check(response)
    return response

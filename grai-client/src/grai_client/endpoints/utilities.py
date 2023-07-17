import datetime
import json
import pathlib
import pprint
import sys
import urllib
import uuid
import warnings
from functools import wraps
from typing import (
    TYPE_CHECKING,
    Any,
    Callable,
    Dict,
    List,
    Literal,
    Optional,
    Type,
    TypeVar,
    Union,
)
from uuid import UUID

import orjson
from grai_schemas.generics import GraiBaseModel, MalformedMetadata
from httpx import Response
from pydantic import BaseModel, ValidationError
from requests import RequestException

from grai_client.errors import InvalidResponseError, ObjectNotFoundError

if sys.version_info < (3, 10):
    from typing_extensions import ParamSpec
else:
    from typing import ParamSpec

if TYPE_CHECKING:
    from grai_client.endpoints.client import BaseClient, ClientOptions


P = ParamSpec("P")
T = TypeVar("T")


def validated_uuid(val: Union[str, UUID]):
    """

    Args:
        val (Union[str, UUID]):

    Returns:

    Raises:

    """
    if isinstance(val, UUID):
        return val

    try:
        return uuid.UUID(str(val))
    except ValueError:
        return None


def is_valid_uuid(val: Union[str, UUID]):
    """

    Args:
        val (Union[str, UUID]):

    Returns:

    Raises:

    """
    if isinstance(val, UUID):
        return True

    try:
        uuid.UUID(str(val))
        return True
    except ValueError:
        return False


def response_status_check(resp: Response) -> Response:
    """

    Args:
        resp (Response):

    Returns:

    Raises:

    """
    if resp.status_code in {200, 201, 204}:
        return resp
    elif resp.status_code == 404:
        raise ObjectNotFoundError(f"Object not found: {resp.url}")
    else:
        message = f"Error: {resp.status_code}. {resp.reason_phrase}. {resp.content.decode()}"

    if resp.status_code == 500:
        message = (
            f"{message}"
            "If you think this should not be the case it might be a bug, you can "
            "submit a bug report at https://github.com/grai-io/grai-core/issues"
        )
    raise RequestException(message)


def orjson_defaults(obj: Any) -> Any:
    """

    Args:
        obj (Any):

    Returns:

    Raises:

    """
    if isinstance(obj, set):
        return list(obj)
    elif isinstance(obj, (pathlib.PosixPath, pathlib.WindowsPath)):
        return str(obj)
    elif isinstance(obj, GraiBaseModel):
        return obj.json()
    elif isinstance(obj, BaseModel):
        return obj.dict()
    else:
        raise Exception(f"No supported JSON serialization format for objects of type {type(obj)}")


class GraiEncoder(json.JSONEncoder):
    """Needed for the base python json implementation"""

    def default(self, obj: Any) -> Any:
        """

        Args:
            obj (Any):

        Returns:

        Raises:

        """
        if isinstance(obj, (UUID, pathlib.PosixPath, pathlib.WindowsPath)):
            return str(obj)
        elif isinstance(obj, (GraiBaseModel, BaseModel)):
            return obj.dict()
        elif isinstance(obj, datetime.date):
            # datetime is a date but date is not a datetime
            # TODO: TZ management
            return obj.isoformat()
        elif isinstance(obj, set):
            return list(obj)
        return json.JSONEncoder.default(self, obj)


def serialize_obj(obj: Dict) -> bytes:
    """

    Args:
        obj (Dict):

    Returns:

    Raises:

    """
    json_obj = orjson.dumps(obj, default=orjson_defaults)
    return json_obj


def serialize_obj_fallback(obj: Dict) -> str:
    """

    Args:
        obj (Dict):

    Returns:

    Raises:

    """
    json_obj = json.dumps(obj, cls=GraiEncoder)
    return json_obj


def add_query_params(url: str, params: dict) -> str:
    """

    Args:
        url (str):
        params (dict):

    Returns:

    Raises:

    """
    url_parts = urllib.parse.urlparse(url)
    query = dict(urllib.parse.parse_qsl(url_parts.query))
    query.update(params)
    return url_parts._replace(query=urllib.parse.urlencode(query)).geturl()


def paginated(
    fn: Callable[["BaseClient", str, "ClientOptions"], Response]
) -> Callable[["BaseClient", str, "ClientOptions"], List[Dict]]:
    @wraps(fn)
    def inner(client: "BaseClient", url: str, options: "ClientOptions") -> List[Dict]:
        """

        Args:
            client:
            url:
            options:
        """
        if page := options.pagination.get("page", False):
            return fn(client, page, options).json()["results"]

        results = []
        page = url
        while page:
            resp = fn(client, page, options).json()

            results.extend(resp["results"])
            page = resp["next"]

        return results

    return inner


def handles_bad_metadata(
    fallback_meta: Type[MalformedMetadata],
) -> Callable[[Callable[[Dict], T]], Callable[[Dict], T]]:
    """

    Args:
        fallback_meta:

    Returns:

    Raises:

    """

    def decorator(fn: Callable[[Dict], T]) -> Callable[[Dict], T]:
        """ """

        @wraps(fn)
        def wrapped(arg: Dict) -> T:
            """

            Args:
                arg:

            Returns:

            Raises:

            """
            try:
                return fn(arg)
            except ValidationError as e:
                new_arg = {**arg}
                metadata = fallback_meta(**new_arg.pop("metadata", {}))
                new_arg["metadata"] = metadata
                try:
                    result = fn(new_arg)
                except Exception:
                    message = (
                        f"Received an invalid object. "
                        f"Normally this is associated with malformed metadata, "
                        f"however, the fallback metadata also failed to parse. This is likely a bug, please "
                        f"submit a bug report at https://github.com/grai-io/grai-core/issues/new. "
                        f"The original object was: \n\n{pprint.pformat(arg)}"
                    )
                    raise Exception(message) from e
                message = (
                    f"Malformed metadata detected in a Grai object Fallback metadata was used but this should be "
                    f"corrected. The problem record was: \n\n{pprint.pformat(arg)}"
                )

                warnings.warn(message)
                return result

        return wrapped

    return decorator


def expects_unique_query(fn) -> Callable[..., T]:
    """"""

    @wraps(fn)
    def wrapper(*args, **kwargs) -> T:
        result = fn(*args, **kwargs)
        if (num_results := len(result)) == 0:
            missing_message = (
                f"A request to `{fn.__name__}{tuple(args)}` was marked as expecting a single unique response. "
                f"However, no results were returned by the server"
            )
            raise ObjectNotFoundError(missing_message)
        elif num_results == 1:
            return result[0]
        else:
            invalid_message = (
                f"A request to `{fn.__name__}{tuple(args)}` was marked as expecting a single unique response ."
                f"However, more than one response was returned."
                f"This is a defensive error which should not be triggered. If you encounter it "
                "please open an issue at www.github.com/grai-io/grai-core/issues"
            )
            raise InvalidResponseError(invalid_message)

    return wrapper

import datetime
import json
import pathlib
import sys
from functools import wraps
from typing import Any, Callable, Dict, List, Type, TypeVar
from uuid import UUID

import orjson
from grai_client.schemas.utilities import GraiBaseModel
from pydantic import BaseModel
from requests import RequestException, Response

if sys.version_info < (3, 10):
    from typing_extensions import ParamSpec
else:
    from typing import ParamSpec


P = ParamSpec("P")
T = TypeVar("T")


def response_status_check(resp: Response) -> Response:
    if resp.status_code in {200, 201}:
        return resp
    elif resp.status_code == 204:
        return resp
    elif resp.status_code == 400:
        message = f"400 Bad request: {str(resp.content)} "
    elif resp.status_code in {401, 403}:
        message = f"Failed to Authenticate with code: {resp.status_code}"
    elif resp.status_code == 404:
        message = f"Error: {resp.status_code}. {resp.reason}"
    elif resp.status_code == 405:
        message = f"{resp.status_code} Operation not permitted: {resp.reason}"
    elif resp.status_code == 415:
        message = f"Error: {resp.status_code}. {resp.reason}"
    elif resp.status_code == 500:
        message = (
            f"Error: {resp.status_code}. {resp.reason} "
            "If you think this should not be the case it might be a bug, you can "
            "submit a bug report at https://github.com/grai-io/grai-core/issues"
        )
    else:
        message = f"No handling for error code {resp.status_code}: {resp.reason}"

    raise RequestException(message)


def orjson_defaults(obj: Any) -> Any:
    if isinstance(obj, set):
        return list(obj)
    elif isinstance(obj, (pathlib.PosixPath, pathlib.WindowsPath)):
        return str(obj)
    elif isinstance(obj, (GraiBaseModel, BaseModel)):
        return obj.dict()
    else:
        raise Exception(
            f"No supported JSON serialization format for objects of type {type(obj)}"
        )


class GraiEncoder(json.JSONEncoder):
    """Needed for the base python json implementation"""

    def default(self, obj: Any) -> Any:
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
    # json_obj = json.dumps(obj, cls=GraiEncoder)
    json_obj = orjson.dumps(obj, default=orjson_defaults)
    return json_obj

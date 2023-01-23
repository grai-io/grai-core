import datetime
import json
import pathlib
import sys
import uuid
from typing import Any, Dict, TypeVar
from uuid import UUID

import orjson
from pydantic import BaseModel
from requests import RequestException, Response

from grai_client.schemas.utilities import GraiBaseModel

if sys.version_info < (3, 10):
    from typing_extensions import ParamSpec
else:
    from typing import ParamSpec


P = ParamSpec("P")
T = TypeVar("T")


def is_valid_uuid(val):
    try:
        uuid.UUID(str(val))
        return True
    except ValueError:
        return False


def response_status_check(resp: Response) -> Response:
    if resp.status_code in {200, 201, 204}:
        return resp

    message = f"Error: {resp.status_code}. {resp.reason}. {resp.content.decode()}"
    if resp.status_code == 500:
        message = (
            f"{message}"
            "If you think this should not be the case it might be a bug, you can "
            "submit a bug report at https://github.com/grai-io/grai-core/issues"
        )

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
    json_obj = orjson.dumps(obj, default=orjson_defaults)
    return json_obj


def serialize_obj_fallback(obj: Dict) -> str:
    json_obj = json.dumps(obj, cls=GraiEncoder)
    return json_obj

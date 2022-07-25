import json
from functools import wraps
from typing import Any, Callable, Dict
from uuid import UUID

from grai_client.schemas.schema import BaseModel
from requests import RequestException, Response
import sys


if sys.version_info < (3, 10):
    from typing_extensions import ParamSpec
else:
    from typing import ParamSpec

P = ParamSpec("P")


def response_status_checker(fn: Callable[P, Response]) -> Callable[P, Dict]:
    def response_status_check(resp: Response) -> Dict:
        if resp.status_code in {200, 201}:
            return resp.json()
        elif resp.status_code == 204:
            return {}
        elif resp.status_code in {400, 401, 402, 403}:
            message = f"Failed to Authenticate with code: {resp.status_code}"
        elif resp.status_code == 404:
            message = resp.reason
        elif resp.status_code == 415:
            message = resp.reason
        elif resp.status_code == 500:
            message = (
                "Hit an internal service error, this looks like a bug, sorry! "
                "Please submit a bug report to https://github.com/grai-io/grai-core/issues"
            )
        else:
            message = f"No handling for error code {resp.status_code}: {resp.reason}"
        raise RequestException(message)

    @wraps(fn)
    def inner(*args: P.args, **kwargs: P.kwargs) -> Dict:
        result = fn(*args, **kwargs)
        response = response_status_check(result)
        return response

    return inner


class GraiEncoder(json.JSONEncoder):
    def default(self, obj: Any) -> Any:
        if isinstance(obj, UUID):
            return str(obj)
        elif isinstance(obj, BaseModel):
            return obj.dict()
        return json.JSONEncoder.default(self, obj)

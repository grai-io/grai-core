from typing import Callable, Dict
from requests import Response
from requests import RequestException
from functools import wraps


def response_status_checker(fn: Callable[[...], Response]) -> Callable[[...], Dict]:
    def response_status_check(resp: Response) -> Response:
        if resp.status_code in {200, 201}:
            return resp
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
            message = f"No handling for error code {resp.status_code}"
        raise RequestException(message)

    @wraps(fn)
    def inner(*args, **kwargs) -> Dict:
        response = response_status_check(fn(*args, **kwargs))
        return response.json()

    return inner

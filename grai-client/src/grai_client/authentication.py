import abc
import json
from typing import Dict, Generator

from httpx import Auth, Request, Response
from pydantic import SecretStr

json_headers = {"accept": "application/json", "Content-Type": "application/json"}


class APIKeyAuth(Auth):
    def __init__(self, api_key: str):
        self.api_key: SecretStr = SecretStr(api_key)

    def auth_flow(self, request: Request) -> Generator[Request, Response, None]:
        request.headers["Authorization"] = f"Api-Key {self.api_key.get_secret_value()}"
        yield request

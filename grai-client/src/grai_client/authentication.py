import abc
import json
from typing import Dict

import requests

json_headers = {"accept": "application/json", "Content-Type": "application/json"}


class AuthHeader(abc.ABC):
    @property
    def headers(self):
        pass


class APIKeyHeader(AuthHeader):
    def __init__(self, api_key: str):
        self.api_key = api_key

    @property
    def headers(self) -> Dict[str, str]:
        return {"Authorization": f"Api-Key {self.api_key}"}

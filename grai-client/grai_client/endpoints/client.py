# from grai_client.authentication import authenticate
from typing import Any
import abc


class BaseClient:
    id = 'base'

    def __init__(self, host: str, port: str):
        self.host = host
        self.port = port
        self.url = f"http://{self.host}:{self.port}"
        self.api = f"{self.url}"

    def build_url(self, endpoint):
        return f"{self.api}{endpoint}"

    # @staticmethod
    # def authentication_headers():
    #     return authenticate()

    def check_authentication(self):
        raise NotImplementedError(f"No authentication implemented for {type(self)}")

    def get(self, arg: Any):
        raise NotImplementedError(f"No get method implemented for type {type(arg)}")

    def post(self, arg: Any, payload: Any = None):
        raise NotImplementedError(f"No post method implemented for type {type(arg)}")

    def patch(self, arg: Any):
        raise NotImplementedError(f"No patch method implemented for type {type(arg)}")

    def delete(self, arg):
        raise NotImplementedError(f"No delete method implemented for type {type(arg)}")


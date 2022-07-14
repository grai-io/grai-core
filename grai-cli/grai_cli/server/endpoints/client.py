from grai_cli import config
from grai_cli.server.authenticate import authenticate
from functools import singledispatchmethod, singledispatch
from typing import Any


class BaseClient():
    def __init__(self):
        self.host = config.grab('server.host')
        self.port = config.grab('server.port')
        self.url = f"http://{self.host}:{self.port}"
        self.api = f"{self.url}"

    def build_url(self, endpoint):
        return f"{self.api}{endpoint}"

    @staticmethod
    def authentication_headers():
        return authenticate()

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


import abc
import json

import requests

json_headers = {"accept": "application/json", "Content-Type": "application/json"}


class AuthHeader(abc.ABC):
    @property
    def headers(self):
        pass


class UserTokenHeader(AuthHeader):
    def __init__(self, token: str):
        self.token = token

    @property
    def headers(self):
        return {"Authorization": f"Token {self.token}"}


class APIKeyHeader(AuthHeader):
    def __init__(self, api_key: str):
        self.api_key = api_key

    @property
    def headers(self):
        return {"Authorization": f"Api-Key {self.api_key}"}


class UserNameHeader(UserTokenHeader):
    def __init__(self, username, password):
        self.username = username
        self.password = password
        super().__init__(token=self.get_token())

    def get_token(self) -> str:
        params = {
            "username": self.username,
            "password": self.password,
        }
        url = "http://localhost:8000/api/v1/auth/api-token/"
        token = requests.post(url, data=json.dumps(params), headers=json_headers)
        if token.status_code != 200:
            raise Exception("Failed to get user token from server")
        return token.json()["token"]

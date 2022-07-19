import requests
import json


json_headers = {
    "accept": "application/json",
    "Content-Type": "application/json"
}


class AuthHeader:
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

    def get_token(self):
        params = {
            "username": self.username,
            "password": self.password,
        }
        url = "http://localhost:8000/api/v1/auth/api-token/"
        token = requests.post(url, data=json.dumps(params), headers=json_headers).json()['token']
        return token

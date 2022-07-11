from grai_cli import config
import requests


class GraiServerConfig:
    json_headers = {
            "accept": "application/json",
            "Content-Type": "application/json"
        }

    def __init__(self):
        server_configs = config.get({
            'server': {
                "host": str,
                "port": str,
            }
        })
        self.host = server_configs['server']['host']
        self.port = server_configs['server']['port']
        self.url = f"http://{self.host}:{self.port}"
        self.api = f"{self.url}"
        self.headers = {}

    def authenticate_with_username(self):
        params = {
            'auth': {
                "username": str,
                "password": str,
            }
        }
        raise Exception("not implemented")
        params = config.get(params)

    def authenticate_with_token(self):
        params = {
            'auth': {"token": str}
        }
        token = config.get(params)
        header = {"Authorization": f"Token {token}"}
        self.headers.update(header)
        return header

    def authenticate_with_api_key(self):
        api_key = config.grab('auth.api_key')
        header = {"Authorization": f"Api-Key {api_key}"}
        self.headers.update(header)
        return header

    def get_jwt(self, username, password):
        response = requests.post(f"{self.api}/token/", headers=self.json_headers, params=self.user_auth_params)
        if response.status_code != 200:
            raise

        return response.json()

    def authenticate(self):
        modes = {
            'username': self.authenticate_with_username,
            'api': self.authenticate_with_api_key
        }
        auth_mode = config.grab('auth.authentication_mode')
        return modes[auth_mode]()


class GraiV1Endpoints(GraiServerConfig):
    base = '/api/v1'
    _is_authenticated = '/auth/is-authenticated/'

    def build_url(self, endpoint):
        return f"{self.api}{self.base}{endpoint}"

    def check_authentication(self):
        url = self.build_url(self._is_authenticated)
        self.headers.update(self.json_headers)
        self.authenticate()
        result = requests.get(url, headers=self.headers)
        return result

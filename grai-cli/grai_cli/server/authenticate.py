from grai_cli import config
import requests
import json


json_headers = {
    "accept": "application/json",
    "Content-Type": "application/json"
}

server_configs = config.get({
    'server': {
        "host": str,
        "port": str,
    }
})


def get_jwt(self, username, password):
    response = requests.post(f"{self.api}/token/", headers=self.json_headers, params=self.user_auth_params)
    if response.status_code != 200:
        raise

    return response.json()


def authenticate_with_username():
    params = {
        "username": config.grab('auth.username'),
        "password": config.grab('auth.password'),
    }
    try:
        token = config['auth']['token'].get(str)
    except:
        url = "http://localhost:8000/api/v1/auth/api-token/"
        token = requests.post(url, data=json.dumps(params), headers=json_headers).json()['token']
        config['auth']['token'].set(token)

    return authenticate_with_token(token)


def authenticate_with_token(token=None):
    token = config.grab('auth.token') if token is None else token
    header = {"Authorization": f"Token {token}"}
    return header


def authenticate_with_api_key():
    api_key = config.grab('auth.api_key')
    header = {"Authorization": f"Api-Key {api_key}"}
    return header


# TODO Switch to pydantic
def authenticate():
    auth_modes = [authenticate_with_api_key, authenticate_with_token, authenticate_with_username]
    for mode in auth_modes:
        try:
            return mode()
        except Exception as e:
            pass

    raise Exception("No supported authentication mode found for your config.")

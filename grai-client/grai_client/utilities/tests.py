import os


def get_test_client():
    from grai_client.endpoints.v1.client import ClientV1

    host = os.environ.get("GRAI_HOST", "localhost")
    port = os.environ.get("GRAI_PORT", "8000")
    username = os.environ.get("GRAI_USERNAME", "null@grai.io")
    password = os.environ.get("GRAI_PASSWORD", "super_secret")
    workspace = os.environ.get("GRAI_WORKSPACE", "default")

    client = ClientV1(host, port, workspace=workspace)
    client.set_authentication_headers(username=username, password=password)
    return client

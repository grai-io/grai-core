import os

def prep_test_auth():
    from grai_cli import config

    host = os.environ.get("GRAI_HOST", None)
    port = os.environ.get("GRAI_PORT", None)

    config["auth"]["username"].set("null@grai.io")
    config["auth"]["password"].set("super_secret")

    if host:
        config["server"]["host"].set(host)
    if port:
        config["server"]["port"].set(port)

def prep_tests():
    prep_test_auth()

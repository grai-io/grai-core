def prep_test_auth():
    from grai_cli import config

    config["auth"]["username"].set("null@grai.io")
    config["auth"]["password"].set("super_secret")


def prep_tests():
    prep_test_auth()

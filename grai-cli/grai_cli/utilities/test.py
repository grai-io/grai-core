import os
import subprocess

from grai_cli.settings.config import BasicAuthSettings, ServerSettingsV1


def prep_test_auth():
    """ """
    from grai_cli import config

    config.server = ServerSettingsV1(host="localhost", port="8000", insecure=True, workspace="default")
    config.auth = BasicAuthSettings(username="null@grai.io", password="super_secret")


def disable_telemetry():
    """ """
    subprocess.run(["grai", "--no-telemetry"])


def prep_tests():
    """ """
    prep_test_auth()
    disable_telemetry()

import os
import subprocess

from grai_cli.settings.config import BasicAuthSettings, ServerSettingsV1


def prep_test_auth():
    """ """
    from grai_cli import config

    config.server = ServerSettingsV1(url="http://localhost:8000", workspace="default/default")
    config.auth = BasicAuthSettings(username="null@grai.io", password="super_secret")


def disable_telemetry():
    """ """
    subprocess.run(["grai", "--no-telemetry"])


def prep_tests():
    """ """
    prep_test_auth()
    disable_telemetry()

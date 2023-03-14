import copy
import os
import uuid

import pytest
from typer.testing import CliRunner

from grai_cli.settings.cache import cache
from grai_cli.settings.config import BasicAuthSettings, ServerSettingsV1, config
from grai_cli.utilities.test import prep_tests


@pytest.fixture(scope="session", autouse=True)
def setup():
    telemetry_state = cache.get("telemetry_consent")
    has_configfile = config.handler.has_config_file
    temp_name = str(uuid.uuid4())

    cache.set("telemetry_consent", False)

    if has_configfile:
        os.rename(config.handler.config_file, temp_name)
    try:
        config.server = ServerSettingsV1(host="localhost", port="8000", insecure=True, workspace="default")
        config.auth = BasicAuthSettings(username="null@grai.io", password="super_secret")
        config.save()
        yield
    finally:
        if has_configfile:
            os.rename(temp_name, config.handler.config_file)
        else:
            os.remove(config.handler.config_file)
        cache.set("telemetry_consent", telemetry_state)


@pytest.fixture
def runner():
    return CliRunner()


@pytest.fixture
def v1_node(runner):
    def make_v1_node():
        node = {
            "version": "v1",
            "type": "Node",
            "spec": {
                "name": "name-" + str(uuid.uuid4()),
                "namespace": "namespace-" + str(uuid.uuid4()),
                "data_source": "test",
            },
        }
        return node

import os

import pytest
from grai_schemas.v1.mock import MockV1
from typer.testing import CliRunner

mocker = MockV1()
organisation = mocker.organisation.organisation_spec(name="default")
workspace = mocker.workspace.workspace_spec(name="default", organisation=organisation)


@pytest.fixture(autouse=True)
def setup():
    """ """
    old_config = os.environ.get("GRAI_CLI_CONFIG_DIR")
    script_dir = os.path.dirname(os.path.realpath(__file__))
    os.environ["GRAI_CLI_CONFIG_DIR"] = os.path.join(script_dir, "config")

    yield

    if old_config is not None:
        os.environ["GRAI_CLI_CONFIG_DIR"] = old_config
    else:
        del os.environ["GRAI_CLI_CONFIG_DIR"]

    # cache.set("telemetry_consent", telemetry_state)


@pytest.fixture()
def config(setup):
    from grai_cli.settings.cache import cache
    from grai_cli.settings.config import GraiConfig

    test_file = os.path.join(os.environ["GRAI_CLI_CONFIG_DIR"], "config.yaml")
    config = GraiConfig.from_file(test_file)
    config.handler.config_file = test_file
    config.handler.config_dir = os.environ["GRAI_CLI_CONFIG_DIR"]
    cache.set("telemetry_consent", False)
    return config


@pytest.fixture(scope="session")
def client():
    from grai_cli.api.server.setup import get_default_client

    return get_default_client()


@pytest.fixture
def mock_v1():
    return MockV1(workspace=workspace)


@pytest.fixture
def runner():
    """ """
    return CliRunner(env=os.environ)


@pytest.fixture
def v1_node(mock_v1):
    """ """
    metadata = {"grai": {"node_type": "Generic"}, "sources": {}}
    node_spec = mock_v1.node.named_node_spec(metadata=metadata, data_sources=[])
    node = mock_v1.node.node(spec=node_spec)
    return node

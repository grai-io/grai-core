import os
import uuid

import pytest
from grai_schemas.v1.mock import MockV1
from typer.testing import CliRunner

from grai_cli.settings.cache import cache
from grai_cli.settings.config import ConfigDirHandler, EnvironmentVariables, GraiConfig


@pytest.fixture(scope="session")
def client():
    from grai_cli.api.server.setup import get_default_client

    return get_default_client()


@pytest.fixture(scope="session")
def organisation():
    return MockV1().organisation.organisation_spec(name="default")


@pytest.fixture(scope="session")
def workspace(client, organisation):
    workspace = client.get(MockV1(organisation=organisation).workspace.workspace_spec(name="default"))
    organisation.id = workspace.spec.organisation
    return workspace


@pytest.fixture(scope="session")
def source(client, workspace):
    source = MockV1(workspace=workspace).source.source_spec(name=f"{uuid.uuid4()}")
    return client.post(source)


@pytest.fixture(autouse=True)
def setup():
    """ """
    old_config = os.environ.get(EnvironmentVariables.config_file, None)
    script_dir = os.path.dirname(os.path.realpath(__file__))
    os.environ[EnvironmentVariables.config_file] = os.path.join(script_dir, "config", "config.yaml")

    yield

    if old_config is not None:
        os.environ[EnvironmentVariables.config_file] = old_config
    else:
        del os.environ[EnvironmentVariables.config_file]


@pytest.fixture()
def config(setup) -> GraiConfig:
    config = GraiConfig()
    cache.set("telemetry_consent", False)
    return config


@pytest.fixture()
def handler(config):
    handler = ConfigDirHandler()
    return handler


@pytest.fixture
def mock_v1(workspace, organisation, source):
    return MockV1(workspace=workspace, organisation=organisation, data_source=source, data_sources=[source])


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

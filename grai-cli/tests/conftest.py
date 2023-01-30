import uuid

import pytest
from typer.testing import CliRunner

from grai_cli.utilities.test import prep_tests

prep_tests()


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

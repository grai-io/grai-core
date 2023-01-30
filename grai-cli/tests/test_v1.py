import os
import pathlib
import tempfile
import uuid

import yaml
from typer.testing import CliRunner

from grai_cli.api.entrypoint import app
from grai_cli.api.server.endpoints import get_nodes
from grai_cli.utilities.test import prep_tests
from grai_cli.utilities.utilities import write_yaml


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


def test_get_by_name_and_namespace(runner):
    with tempfile.NamedTemporaryFile("w+") as file:
        node_dict = make_v1_node()
        name = node_dict["spec"]["name"]
        namespace = node_dict["spec"]["namespace"]
        write_yaml(node_dict, file.name)
        result = runner.invoke(app, ["apply", file.name])
        result = get_nodes(name=name, namespace=namespace, print=False)
        assert len(result) == 1

import os
import pathlib
import tempfile
import uuid

import yaml
from grai_schemas.v1 import NodeV1
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
        assert isinstance(result, NodeV1)
        assert result.spec.name == name and result.spec.namespace == namespace


def test_get_by_namespace(runner):
    with tempfile.NamedTemporaryFile("w+") as file:
        node_dict = make_v1_node()
        namespace = node_dict["spec"]["namespace"]
        write_yaml(node_dict, file.name)
        result = runner.invoke(app, ["apply", file.name])
        results = get_nodes(namespace=namespace, print=False)
        assert isinstance(results, list)
        assert all(isinstance(result, NodeV1) for result in results)
        assert all(result.spec.namespace == namespace for result in results)

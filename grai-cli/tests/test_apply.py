import os
import pathlib
import tempfile
import uuid

import yaml
from grai_schemas.v1.mock import MockV1
from typer.testing import CliRunner

from grai_cli.api.entrypoint import app
from grai_cli.api.server.endpoints import apply, delete, get_edges, get_nodes
from grai_cli.utilities.test import prep_tests
from grai_cli.utilities.utilities import write_yaml


def get_temp_file():
    """ """
    fname = os.urandom(24).hex()
    return os.path.join(tempfile.gettempdir(), fname)


def test_apply_single_node(runner, v1_node):
    """

    Args:
        runner:

    Returns:

    Raises:

    """

    with tempfile.NamedTemporaryFile("w+") as file:
        node = MockV1().node.node()
        write_yaml(node, file.name)
        result = runner.invoke(app, ["apply", file.name])
        assert result.exit_code == 0, result


def test_apply_multi_node(runner):
    """

    Args:
        runner:

    Returns:

    Raises:

    """
    with tempfile.NamedTemporaryFile("w+") as file:
        file_name = pathlib.Path(file.name)
        nodes = [make_v1_node() for i in range(5)]
        write_yaml(nodes, file.name)
        result = runner.invoke(app, ["apply", file.name])
        assert result.exit_code == 0, result


def test_create_and_get_nodes(runner):
    """

    Args:
        runner:

    Returns:

    Raises:

    """
    with tempfile.NamedTemporaryFile("w+") as file:
        nodes = [make_v1_node() for i in range(2)]
        write_yaml(nodes, file.name)
        result = runner.invoke(app, ["apply", file.name])
        assert result.exit_code == 0
        server_nodes = get_nodes(print=False)
        node_set = {(str(n.spec.name), str(n.spec.namespace)) for n in server_nodes}
        original_node_set = {(n["spec"]["name"], n["spec"]["namespace"]) for n in nodes}
        diff = original_node_set - node_set
        assert len(diff) == 0, "Created nodes were not returned by get"


def test_delete_single_node(runner):
    """

    Args:
        runner:

    Returns:

    Raises:

    """
    with tempfile.NamedTemporaryFile("w+") as file:
        file_name = pathlib.Path(file.name)
        node_dict = make_v1_node()
        yaml.dump(node_dict, file)
        result = runner.invoke(app, ["apply", file.name])
        assert result.exit_code == 0, result
        result = runner.invoke(app, ["delete", file.name])
        assert result.exit_code == 0, result
        server_nodes = get_nodes(print=False)
        node_set = {(str(n.spec.name), str(n.spec.namespace)) for n in server_nodes}
        assert (
            node_dict["spec"]["name"],
            node_dict["spec"]["namespace"],
        ) not in node_set

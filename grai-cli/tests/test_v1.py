import tempfile

from grai_schemas.v1 import NodeV1

from grai_cli.api.entrypoint import app
from grai_cli.api.server.endpoints import apply, perform_type_query
from grai_cli.utilities.utilities import write_yaml


def test_get_by_name_and_namespace(runner, v1_node):
    """

    Args:
        runner:

    Returns:

    Raises:

    """
    with tempfile.NamedTemporaryFile("w+") as file:
        node_dict = v1_node.dict()
        name = v1_node.spec.name
        namespace = v1_node.spec.namespace

        write_yaml(node_dict, file.name)

        result = runner.invoke(app, ["apply", file.name])
        results = perform_type_query(name=name, namespace=namespace, print=False)

        assert len(results) > 0
        for result in results:
            assert isinstance(result, NodeV1)
            assert result.spec.name == name and result.spec.namespace == namespace


def test_get_by_namespace(runner, v1_node):
    """

    Args:
        runner:

    Returns:

    Raises:

    """
    with tempfile.NamedTemporaryFile("w+") as file:
        node_dict = v1_node.dict()
        namespace = node_dict["spec"]["namespace"]
        write_yaml(node_dict, file.name)
        result = runner.invoke(app, ["apply", file.name])
        results = perform_type_query(namespace=namespace, print=False)
        assert isinstance(results, list)
        assert all(isinstance(result, NodeV1) for result in results)
        assert all(result.spec.namespace == namespace for result in results)

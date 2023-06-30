import os
import uuid

import pandas as pd
import pytest
from grai_schemas.v1.source import SourceSpec
from grai_schemas.v1.workspace import WorkspaceSpec

from grai_source_flat_file.base import FlatFileIntegration

# @pytest.fixture
# def client():
#     client = ClientV1("localhost", "8000", workspace="default")
#     client.authenticate(username="null@grai.io", password="super_secret")
#     return client


@pytest.fixture
def default_workspace():
    return WorkspaceSpec(name="default", organization="default")


@pytest.fixture
def mock_source(default_workspace):
    return SourceSpec(name="SnowflakeTest", workspace=default_workspace)


@pytest.fixture
def mock_data():
    """ """
    n = 10
    test_data = {"a": range(n), "b": ["t"] * n}
    return pd.DataFrame(test_data)


class MockClient:
    def __init__(self):
        self.id = "v1"

    def get(self, type, **kwargs):
        return SourceSpec(id=uuid.uuid4(), **kwargs)


@pytest.fixture
def mock_get_nodes_and_edges(mock_data):
    """

    Args:
        mock_data:

    Returns:

    Raises:

    """
    file_name = "test.csv"
    namespace = "test"

    try:
        mock_data.to_csv(file_name, index=False)

        integration = FlatFileIntegration.from_client(
            client=MockClient(),
            source_name="test",
            file_name=file_name,
            namespace=namespace,
        )

        nodes, edges = integration.get_nodes_and_edges()
    except Exception as e:
        raise e
    finally:
        os.remove(file_name)
    return nodes, edges

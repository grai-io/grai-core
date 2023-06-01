import os

import pandas as pd
import pytest
from grai_client.endpoints.v1.client import ClientV1

from grai_source_flat_file.base import get_nodes_and_edges

# @pytest.fixture
# def client():
#     client = ClientV1("localhost", "8000", workspace="default")
#     client.authenticate(username="null@grai.io", password="super_secret")
#     return client


@pytest.fixture
def mock_data():
    """ """
    n = 10
    test_data = {"a": range(n), "b": ["t"] * n}
    return pd.DataFrame(test_data)


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
        nodes, edges = get_nodes_and_edges(file_name, namespace)
    except Exception as e:
        raise e
    finally:
        os.remove(file_name)
    return nodes, edges

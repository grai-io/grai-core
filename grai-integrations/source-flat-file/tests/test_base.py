import os

import pandas as pd
from grai_client.endpoints.v1.client import ClientV1
from grai_schemas import config as core_config

from grai_source_flat_file.adapters import adapt_to_client
from grai_source_flat_file.loader import build_nodes_and_edges


def test_build_nodes(mock_data):
    file_name = "test.csv"
    namespace = "test"
    mock_data.to_csv(file_name, index=False)
    try:
        nodes, edges = build_nodes_and_edges(file_name, namespace)
    except Exception as e:
        raise e
    finally:
        os.remove(file_name)


def test_adapt_nodes(mock_data):
    file_name = "test.csv"
    namespace = "test"
    mock_data.to_csv(file_name, index=False)
    try:
        nodes, edges = build_nodes_and_edges(file_name, namespace)
        nodes = adapt_to_client(nodes)
    except Exception as e:
        raise e
    finally:
        os.remove(file_name)

from grai_source_flat_file.loader import get_nodes_and_edges
from grai_source_flat_file.adapters import adapt_to_client
from grai_source_flat_file.base import update_server
import pandas as pd
import os


n = 10
test_data = {
    'a': range(n),
    'b': ['t'] * n
}
test_data = pd.DataFrame(test_data)


def test_load():
    import grai_source_flat_file


def test_build_nodes():
    file_name = 'test.csv'
    namespace = 'test'
    test_data.to_csv(file_name, index=False)
    try:
        nodes, edges = get_nodes_and_edges(file_name, namespace)
    except Exception as e:
        raise e
    finally:
        os.remove(file_name)


def test_adapt_nodes():
    file_name = 'test.csv'
    namespace = 'test'
    test_data.to_csv(file_name, index=False)
    try:
        nodes, edges = get_nodes_and_edges(file_name, namespace)
        nodes = adapt_to_client(nodes)
    except Exception as e:
        raise e
    finally:
        os.remove(file_name)

def test_update_server_nodes():
    file_name = 'test.csv'
    namespace = 'test'
    test_data.to_csv(file_name, index=False)
    
    try:
        update_server(file_name, namespace)
    except Exception as e:
        raise e
    finally:
        os.remove(file_name)




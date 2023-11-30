import os

from grai_source_flat_file.adapters import adapt_to_client
from grai_source_flat_file.loader import build_nodes_and_edges


class TestFileTypes:
    def test_parquet(self, mock_data):
        file_name = "test.parquet"
        namespace = "test"
        table_name, extension = os.path.splitext(file_name)
        mock_data.to_parquet(file_name, index=False)
        try:
            nodes, edges = build_nodes_and_edges(file_name, extension, table_name, file_name, namespace)
        except Exception as e:
            raise e
        finally:
            os.remove(file_name)

    def test_csv(self, mock_data):
        """

        Args:
            mock_data:

        Returns:

        Raises:

        """
        file_name = "test.csv"
        table_name, extension = os.path.splitext(file_name)
        namespace = "test"
        mock_data.to_csv(file_name, index=False)
        try:
            nodes, edges = build_nodes_and_edges(file_name, extension, table_name, file_name, namespace)
        except Exception as e:
            raise e
        finally:
            os.remove(file_name)

    def test_feather(self, mock_data):
        """

        Args:
            mock_data:

        Returns:

        Raises:

        """
        file_name = "test.feather"
        table_name, extension = os.path.splitext(file_name)
        namespace = "test"
        mock_data.to_feather(file_name)
        try:
            nodes, edges = build_nodes_and_edges(file_name, extension, table_name, file_name, namespace)
        except Exception as e:
            raise e
        finally:
            os.remove(file_name)


def test_adapt_nodes(mock_data, mock_source):
    """

    Args:
        mock_data:

    Returns:

    Raises:

    """
    file_name = "test.csv"
    table_name, extension = os.path.splitext(file_name)
    namespace = "test"
    mock_data.to_csv(file_name, index=False)
    try:
        nodes, edges = build_nodes_and_edges(file_name, extension, table_name, file_name, namespace)
        nodes = adapt_to_client(nodes, mock_source, "v1")
    except Exception as e:
        raise e
    finally:
        os.remove(file_name)

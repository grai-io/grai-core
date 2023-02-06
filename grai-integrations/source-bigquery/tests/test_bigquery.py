import os
import unittest

import pytest

from grai_source_bigquery.loader import BigqueryConnector

has_dotenv_file = os.path.exists(".env")

if has_dotenv_file:
    from dotenv import load_dotenv

    load_dotenv(".env")
    connection = BigqueryConnector()


def test_connector_from_env_vars():
    env_vars = {
        "GRAI_BIGQUERY_PROJECT": "thing",
        "GRAI_BIGQUERY_DATASET": "grai",
        "GRAI_BIGQUERY_CREDENTIALS": "user",
    }
    for k, v in env_vars.items():
        os.environ[k] = v

    conn = BigqueryConnector()
    assert conn.project == "thing"
    assert conn.dataset == "grai"
    assert conn.credentials == "user"


class TestLiveBigqueryIfHasDotEnv(unittest.TestCase):
    run_tests = has_dotenv_file

    @classmethod
    def test_building_nodes(cls):
        if not cls.run_tests:
            return

        with connection.connect() as conn:
            tables = conn.get_tables()

        assert isinstance(tables, list)
        # assert len(tables) > 0, f"test expected more than {len(tables)} results"

    @classmethod
    def test_building_edges(cls):
        if not cls.run_tests:
            return

        with connection.connect() as conn:
            edges = conn.get_foreign_keys()

        assert isinstance(edges, list)
        # assert len(edges) > 0, f"test expected more than {len(edges)} results"

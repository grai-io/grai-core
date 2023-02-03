import os
import unittest

import pytest

from grai_source_snowflake.loader import SnowflakeConnector

has_dotenv_file = os.path.exists(".env")

if has_dotenv_file:
    from dotenv import load_dotenv

    load_dotenv(".env")
    connection = SnowflakeConnector()


def test_connector_from_env_vars():
    env_vars = {
        "GRAI_SNOWFLAKE_ACCOUNT": "thing",
        "GRAI_SNOWFLAKE_DATABASE": "grai",
        "GRAI_SNOWFLAKE_USER": "user",
        "GRAI_SNOWFLAKE_PASSWORD": "pw",
        "GRAI_SNOWFLAKE_ROLE": "baller",
        "GRAI_SNOWFLAKE_WAREHOUSE": "its-huge",
        "GRAI_SNOWFLAKE_SCHEMA": "PUBLIC",
    }
    for k, v in env_vars.items():
        os.environ[k] = v

    conn = SnowflakeConnector()
    assert conn.user == "user"
    assert conn.password == "pw"
    assert conn.account == "thing"
    assert conn.database == "grai"
    assert conn.role == "baller"
    assert conn.warehouse == "its-huge"
    assert conn.schema == "PUBLIC"


class TestLiveSnowflakeIfHasDotEnv(unittest.TestCase):
    run_tests = has_dotenv_file

    @classmethod
    def test_building_nodes(cls):
        if not cls.run_tests:
            return

        with connection.connect() as conn:
            tables = conn.tables

        assert isinstance(tables, list)
        # assert len(tables) > 0, f"test expected more than {len(tables)} results"

    @classmethod
    def test_building_edges(cls):
        if not cls.run_tests:
            return

        with connection.connect() as conn:
            edges = conn.foreign_keys

        assert isinstance(edges, list)
        # assert len(edges) > 0, f"test expected more than {len(edges)} results"

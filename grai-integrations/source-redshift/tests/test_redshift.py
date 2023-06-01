import os

import pytest

from grai_source_redshift.loader import RedshiftConfig, RedshiftConnector


def test_building_nodes(connection):
    """

    Args:
        connection:

    Returns:

    Raises:

    """
    with connection.connect() as conn:
        tables = conn.tables

    assert len(tables) > 0


def test_building_edges(connection):
    """

    Args:
        connection:

    Returns:

    Raises:

    """
    with connection.connect() as conn:
        edges = conn.foreign_keys

    assert len(edges) > 0, edges


def test_config_from_env_vars():
    """ """
    env_vars = {
        "GRAI_REDSHIFT_HOST": "localhost",
        "GRAI_REDSHIFT_DATABASE": "grai",
        "GRAI_REDSHIFT_USER": "user",
        "GRAI_REDSHIFT_PASSWORD": "pw",
        "GRAI_REDSHIFT_PORT": "8000",
    }
    for k, v in env_vars.items():
        os.environ[k] = v

    conf = RedshiftConfig()
    assert conf.host == "localhost"
    assert conf.port == 8000
    assert conf.database == "grai"
    assert conf.user == "user"
    assert conf.password.get_secret_value() == "pw"

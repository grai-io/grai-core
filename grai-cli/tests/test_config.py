import importlib
import os
import uuid

import grai_cli


def test_missing_config_file():
    """config loads even without config file"""
    if not os.path.exists(grai_cli.config.handler.config_file):
        # Config file doesn't exist and the package loaded, all good I guess.
        return

    file_name = str(uuid.uuid4())
    os.rename(grai_cli.config.handler.config_file, file_name)
    try:
        importlib.reload(grai_cli)
        # grai_cli.settings.config.GraiConfig()
    except:
        raise
    finally:
        os.rename(file_name, grai_cli.config.handler.config_file)


def test_default_config_values():
    """Package loads correct default config values"""
    default_host = grai_cli.config.server.host
    default_port = grai_cli.config.server.port

    assert default_host == "localhost"
    assert default_port == "8000"

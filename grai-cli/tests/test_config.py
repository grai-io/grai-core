import importlib
import os
import uuid

import grai_cli


def test_missing_config_file(config):
    """config loads even without config file"""
    if not os.path.exists(config.handler.config_file):
        # Config file doesn't exist and the package loaded, all good I guess.
        return

    file_name = str(uuid.uuid4())
    os.rename(config.handler.config_file, file_name)
    try:
        importlib.reload(grai_cli)
        # grai_cli.settings.config.GraiConfig()
    except:
        raise
    finally:
        os.rename(file_name, config.handler.config_file)


def test_default_config_values(config):
    """Package loads correct default config values"""
    default_url = config.server.url

    assert default_url == "http://localhost:8000"

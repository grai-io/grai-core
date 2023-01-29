import importlib
import os

import grai_cli


def test_missing_config_file():
    """Package loads even without config file"""
    if not os.path.exists(grai_cli.config.config_filename):
        # Config file doesn't exist and the package loaded, all good I guess.
        return

    os.rename(grai_cli.config.config_filename, "temp")
    try:
        importlib.reload(grai_cli)
        grai_cli.config.reload()
    except:
        raise
    finally:
        if os.path.exists("temp") and not os.path.exists(grai_cli.config.config_filename):
            os.rename("temp", grai_cli.config.config_filename)


def test_default_config_values():
    """Package loads correct default config values"""
    default_host = grai_cli.config["server"]["host"].get(str)
    default_port = grai_cli.config["server"]["port"].get(str)

    assert default_host == "localhost"
    assert default_port == "8000"

from typing import Callable
import yaml
from pathlib import Path
from functools import wraps
from grai_cli.settings.config import config


def load_yaml(file: str | Path):
    with open(file, "r") as file:
        result = yaml.safe_load(file)
    return result


def writes_config(fn: Callable) -> Callable:
    @wraps(fn)
    def inner(*args, **kwargs):
        write_config = kwargs.pop('write_config', True)
        config_location = kwargs.pop('config_location', config.config_filename)

        result = fn(*args, **kwargs)
        if write_config:
            with open(config_location, 'w') as file:
                file.write(config.dump(redact=False))
        return result
    return inner


def get_config_view(config_field: str):
    """Assumes <config_field> is dot separated i.e. `auth.username`"""
    config_view = config.root()
    for path in config_field.split('.'):
        config_view = config_view[path]
    return config_view

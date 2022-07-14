from typing import Callable, Dict, Iterable
import yaml
from pathlib import Path
from functools import wraps
from grai_cli.settings.config import config


def load_yaml(file: str | Path) -> Dict:
    with open(file, "r") as file:
        result = yaml.safe_load(file)
    return result


def load_all_yaml(file: str | Path) -> Iterable[Dict]:
    with open(file, "r") as file:
        for item in yaml.safe_load_all(file):
            yield item


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

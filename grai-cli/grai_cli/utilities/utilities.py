import yaml
from pydantic import BaseModel
from pathlib import Path
from functools import wraps, singledispatch
from grai_cli.settings.config import config
from typing import Dict, Any, List, Tuple, Union, Callable, Iterable
from io import TextIOWrapper


def load_yaml(file: str | Path) -> Dict:
    with open(file, "r") as file:
        result = yaml.safe_load(file)
    return result


def load_all_yaml(file: str | Path) -> Iterable[Dict]:
    with open(file, "r") as file:
        for item in yaml.safe_load_all(file):
            yield item


def file_handler(fn):
    def inner(*args, **kwargs):
        pass


@singledispatch
def write_yaml(data: Any, path: str | Path, mode: str):
    raise NotImplementedError()


@write_yaml.register
def _(data: dict, file: Union[str, Path, TextIOWrapper], mode: str = "w"):
    if isinstance(file, (str, Path)):
        with open(file, mode) as f:
            yaml.dump(data, f)
    else:
        yaml.dump(data, file)


@write_yaml.register
def _(data: BaseModel, file: Union[str, Path, TextIOWrapper], mode: str = "w"):
    write_yaml(data.dict(), file, mode)


@write_yaml.register
def _(data: list, file: str | Path, mode: str = "w"):
    n = len(data)
    if n == 0:
        return
    elif n == 1:
        write_yaml(data[0], file, mode)
    else:
        with open(file, mode) as f:
            write_yaml(data[0], f)
            for item in data[1:]:
                f.write("---\n")
                write_yaml(item, f)


def writes_config(fn: Callable) -> Callable:
    @wraps(fn)
    def inner(*args, **kwargs):
        write_config = kwargs.pop("write_config", True)
        config_location = kwargs.pop("config_location", config.config_filename)

        result = fn(*args, **kwargs)
        if write_config:
            with open(config_location, "w") as file:
                file.write(config.dump(redact=False))
        return result

    return inner


def get_config_view(config_field: str):
    """Assumes <config_field> is dot separated i.e. `auth.username`"""
    config_view = config.root()
    for path in config_field.split("."):
        config_view = config_view[path]
    return config_view

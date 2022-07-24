from functools import singledispatch, wraps
from io import TextIOBase, TextIOWrapper
from pathlib import Path
from typing import Any, Callable, Dict, Iterable, List, Tuple, Union
from uuid import UUID

import yaml
from grai_cli.settings.config import config
from pydantic import BaseModel


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
def prep_data(data: Any):
    return data


@prep_data.register
def _(data: dict) -> Dict:
    return {k: prep_data(v) for k, v in data.items()}


@prep_data.register
def _(data: UUID) -> str:
    return str(data)


@prep_data.register
def _(data: BaseModel) -> Dict:
    return prep_data(data.dict())


@prep_data.register
def _(data: list) -> List[Dict]:
    return [prep_data(item) for item in data]


def write_yaml(
    data: Union[List, Dict, BaseModel],
    path: Union[str, Path, TextIOWrapper, TextIOBase],
    mode: str = "w",
):
    data = prep_data(data)
    dumper = yaml.dump_all if isinstance(data, list) else yaml.dump
    if isinstance(path, (str, Path)):
        with open(path, mode) as f:
            dumper(data, f)
    else:
        dumper(data, path)


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


def merge_dicts(dict_a: Dict, dict_b: Dict) -> Dict:
    """Recursively merge elements of dict b into dict a preferring b"""
    for k, v in dict_b.items():
        if isinstance(dict_a.get(k, None), dict) and isinstance(v, dict):
            merge_dicts(dict_a[k], v)
        else:
            dict_a[k] = v
    return dict_a

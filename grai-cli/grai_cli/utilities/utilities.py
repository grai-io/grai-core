from functools import singledispatch, wraps
from io import TextIOBase, TextIOWrapper
from pathlib import Path
from tempfile import NamedTemporaryFile, TemporaryFile
from typing import (
    IO,
    Any,
    Callable,
    Dict,
    Iterable,
    List,
    Sequence,
    TextIO,
    Tuple,
    Union,
)
from uuid import UUID

import yaml
from multimethod import multimethod
from pydantic import BaseModel

from grai_cli.settings.config import config


def load_yaml(file: Union[str, TextIOBase]) -> Dict:
    if isinstance(file, str):
        with open(file, "r") as file:
            result = yaml.safe_load(file)
    else:
        result = yaml.safe_load(file)
    return result


def load_all_yaml(file: Union[str, TextIOBase]) -> Iterable[Dict]:
    if isinstance(file, str):
        with open(file, "r") as file:
            for item in yaml.safe_load_all(file):
                yield item
    else:
        for item in yaml.safe_load_all(file):
            yield item


@multimethod
def prep_data(data: Any) -> Any:
    return data


@prep_data.register
def _(data: Dict) -> Dict:
    return {k: prep_data(v) for k, v in data.items()}


@prep_data.register
def _(data: UUID) -> str:
    return str(data)


@prep_data.register
def _(data: BaseModel) -> Dict:
    return prep_data(data.dict())


@prep_data.register
def _(data: List) -> List[Dict]:
    return [prep_data(item) for item in data]


@multimethod
def dump_yaml():
    raise NotImplementedError()


@dump_yaml.register
def dump_individual_yaml(item: Dict, stream: TextIOBase):
    yaml.safe_dump(item, stream)


@dump_yaml.register
def dump_model_yaml(item: BaseModel, stream: TextIOBase):
    dump_yaml(item.dict(), stream)


@dump_yaml.register
def dump_multiple_yaml(items: Sequence[Dict], stream: TextIOBase):
    yaml.safe_dump_all(items, stream)


@dump_yaml.register
def dump_multiple_yaml(items: Sequence[BaseModel], stream: TextIOBase):
    yaml.safe_dump_all(list(item.dict() for item in items), stream)


def write_yaml(
    data: Union[Sequence, Dict, BaseModel],
    path: Union[str, Path, TextIOBase],
    mode: str = "w",
):
    data = prep_data(data)

    if isinstance(path, (str, Path)):
        with open(path, mode) as f:
            dump_yaml(data, f)
    else:
        dump_yaml(data, path)


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

import importlib.util
from functools import wraps
from io import TextIOBase
from pathlib import Path
from typing import IO, Any, Callable, Dict, Iterable, List, Sequence, Union
from uuid import UUID

import typer
import yaml
from multimethod import multimethod
from pydantic import BaseModel

from grai_cli.settings.config import config

HAS_RICH = importlib.util.find_spec("rich") is not None

if HAS_RICH:
    from rich import print
else:
    print = print


def default_callback(ctx: typer.Context):
    """

    Args:
        ctx (typer.Context):

    Returns:

    Raises:

    """
    ctx.meta.setdefault("command_path", [])
    if ctx.invoked_subcommand is not None:
        ctx.meta["command_path"].append(ctx.invoked_subcommand)


def load_yaml(file: Union[str, TextIOBase]) -> Dict:
    """

    Args:
        file (Union[str, TextIOBase]):

    Returns:

    Raises:

    """
    if isinstance(file, str):
        with open(file, "r") as file:
            result = yaml.safe_load(file)
    else:
        result = yaml.safe_load(file)
    return result


def load_all_yaml(file: Union[str, TextIOBase]) -> Iterable[Dict]:
    """

    Args:
        file (Union[str, TextIOBase]):

    Returns:

    Raises:

    """
    if isinstance(file, str):
        with open(file, "r") as file:
            for item in yaml.safe_load_all(file):
                yield item
    else:
        for item in yaml.safe_load_all(file):
            yield item


@multimethod
def prep_data(data: Any) -> Any:
    """

    Args:
        data (Any):

    Returns:

    Raises:

    """
    return data


@prep_data.register
def _(data: Dict) -> Dict:
    """

    Args:
        data (Dict):

    Returns:

    Raises:

    """
    return {k: prep_data(v) for k, v in data.items()}


@prep_data.register
def _(data: UUID) -> str:
    """

    Args:
        data (UUID):

    Returns:

    Raises:

    """
    return str(data)


@prep_data.register
def _(data: BaseModel) -> Dict:
    """

    Args:
        data (BaseModel):

    Returns:

    Raises:

    """
    return prep_data(data.dict())


@prep_data.register
def _(data: List) -> List[Dict]:
    """

    Args:
        data (List):

    Returns:

    Raises:

    """
    return [prep_data(item) for item in data]


@multimethod
def dump_yaml():
    """ """
    raise NotImplementedError()


@dump_yaml.register
def dump_individual_yaml(item: Dict, stream: TextIOBase):
    """

    Args:
        item (Dict):
        stream (TextIOBase):

    Returns:

    Raises:

    """
    yaml.safe_dump(item, stream)


@dump_yaml.register
def dump_model_yaml(item: BaseModel, stream: TextIOBase):
    """

    Args:
        item (BaseModel):
        stream (TextIOBase):

    Returns:

    Raises:

    """
    dump_yaml(item.dict(), stream)


@dump_yaml.register
def dump_multiple_yaml(items: Sequence[Dict], stream: TextIOBase):
    """

    Args:
        items (Sequence[Dict]):
        stream (TextIOBase):

    Returns:

    Raises:

    """
    yaml.safe_dump_all(items, stream)


@dump_yaml.register
def dump_multiple_yaml(items: Sequence[BaseModel], stream: TextIOBase):
    """

    Args:
        items (Sequence[BaseModel]):
        stream (TextIOBase):

    Returns:

    Raises:

    """
    yaml.safe_dump_all(list(item.dict() for item in items), stream)


def write_yaml(
    data: Union[Sequence, Dict, BaseModel],
    path: Union[str, Path, TextIOBase],
    mode: str = "w",
):
    """

    Args:
        data (Union[Sequence, Dict, BaseModel]):
        path (Union[str, Path, TextIOBase]):
        mode (str, optional):  (Default value = "w")

    Returns:

    Raises:

    """
    data = prep_data(data)

    if isinstance(path, (str, Path)):
        with open(path, mode) as f:
            dump_yaml(data, f)
    else:
        dump_yaml(data, path)


# def writes_config(fn: Callable) -> Callable:
#     @wraps(fn)
#     def inner(*args, **kwargs):
#         write_config = kwargs.pop("write_config", True)
#         config_location = kwargs.pop("config_location", config.handler.config_file)
#
#         result = fn(*args, **kwargs)
#         if write_config:
#             with open(config_location, "w") as file:
#                 file.write(config.dump(redact=False))
#         return result
#
#     return inner


def get_config_view(config_field: str):
    """Assumes <config_field> is dot separated i.e. `auth.username`

    Args:
        config_field (str):

    Returns:

    Raises:

    """
    config_view = config.root()
    for path in config_field.split("."):
        config_view = config_view[path]
    return config_view


def merge_dicts(dict_a: Dict, dict_b: Dict) -> Dict:
    """Recursively merge elements of dict b into dict a preferring b

    Args:
        dict_a (Dict):
        dict_b (Dict):

    Returns:

    Raises:

    """
    for k, v in dict_b.items():
        if isinstance(dict_a.get(k, None), dict) and isinstance(v, dict):
            merge_dicts(dict_a[k], v)
        else:
            dict_a[k] = v
    return dict_a

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

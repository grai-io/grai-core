import pathlib
from typing import Any

import orjson
from pydantic.json import pydantic_encoder


def orjson_defaults(obj: Any) -> Any:
    """

    Args:
        obj (Any):

    Returns:

    Raises:

    """
    if isinstance(obj, set):
        return list(obj)
    elif isinstance(obj, (pathlib.PosixPath, pathlib.WindowsPath)):
        return str(obj)
    else:
        raise Exception(f"No supported JSON serialization format for objects of type {type(obj)}")


def dump_json(v, *, default):
    return orjson.dumps(v, default=default, option=orjson.OPT_NON_STR_KEYS).decode()


def load_json(*args, **kwargs):
    return orjson.loads(*args, **kwargs)

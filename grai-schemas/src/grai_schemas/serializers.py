import json
import os
import pathlib
from pathlib import Path
from typing import IO, Any, Dict, Iterable, List, Optional, Sequence, Type, Union

import orjson
import yaml
from pydantic import BaseModel
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


def dump_json(v, *, default) -> str:
    return orjson.dumps(v, default=default, option=orjson.OPT_NON_STR_KEYS).decode()


def load_json(*args, **kwargs):
    return orjson.loads(*args, **kwargs)


class GraiYamlSerializer:
    @staticmethod
    def load(stream: Union[str, Path, IO]) -> Union[Dict, List[Dict]]:
        """

        Args:
            stream:

        Returns:

        Raises:

        """
        if isinstance(stream, Path):
            with open(stream, "r") as file:
                result = list(yaml.safe_load_all(file))
        elif isinstance(stream, str) and (stream.endswith((".yml", ".yaml")) or os.path.exists(stream)):
            with open(stream, "r") as file:
                result = list(yaml.safe_load_all(file))
        else:
            result = list(yaml.safe_load_all(stream))

        if len(result) == 1:
            result = result[0]

        return result

    @classmethod
    def dump(cls, item: Any, stream: Optional[Union[IO, str, Path]] = None) -> str:
        """

        Args:
            item:
            stream:

        Returns:

        Raises:

        """
        # re-use the json serializers for compatability
        prepped_data = cls.prep_data(item)
        dumper = yaml.safe_dump_all if isinstance(item, Sequence) else yaml.safe_dump

        if stream is None:
            result = dumper(prepped_data)
        elif isinstance(stream, (str, Path)):
            with open(stream, "w") as file:
                result = dumper(prepped_data, file)
        else:
            result = dumper(prepped_data, stream)

        return result

    @staticmethod
    def prep_data(data: Any) -> Union[str, List[str]]:
        """

        Args:
            data (Any):

        Returns:

        Raises:

        """
        if isinstance(data, Sequence):
            return list(load_json(dump_json(item, default=orjson_defaults)) for item in data)
        else:
            return load_json(dump_json(data, default=orjson_defaults))

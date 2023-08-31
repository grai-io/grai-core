import json
import os
import pathlib
from datetime import date, datetime, timezone
from enum import Enum
from json import JSONEncoder
from pathlib import Path
from typing import (
    IO,
    Any,
    Callable,
    Dict,
    Iterable,
    List,
    Optional,
    Sequence,
    Type,
    Union,
)
from uuid import UUID

import yaml
from pydantic import BaseModel
from pydantic.json import pydantic_encoder


def to_ecma262(dt: datetime) -> str:
    # compatible with Django defaults
    dt_utc = dt.astimezone(timezone.utc)
    return dt_utc.strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z"


class GraiEncoder(JSONEncoder):
    def default(self, obj: Any):
        if isinstance(obj, Enum):
            return obj.value
        elif isinstance(obj, BaseModel):
            return obj.dict()
        elif isinstance(obj, (UUID, pathlib.PosixPath, pathlib.WindowsPath)):
            return str(obj)
        elif isinstance(obj, datetime):
            return to_ecma262(obj)
        elif isinstance(obj, date):
            return obj.strftime("%Y-%m-%d")
        elif isinstance(obj, set):
            return list(obj)

        return super().default(obj)


encoder = GraiEncoder()


def dump_json(v, *, default: Optional[Callable] = None) -> str:
    if default is None:
        return json.dumps(v, cls=GraiEncoder)
    else:
        return json.dumps(v, default=default, cls=GraiEncoder)


def load_json(v):
    return json.loads(v)


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
            return list(load_json(dump_json(item)) for item in data)
        else:
            return load_json(dump_json(data))

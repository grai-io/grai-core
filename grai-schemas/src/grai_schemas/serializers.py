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
    """Convert a datetime to a string in ECMA-262 format

    This function aims to maintain compatibility with Django default datetime behavior which itself follows the ECMA-262 standard.

    Args:
        dt: The datetime to convert

    Returns:
        The datetime in ECMA-262 format
    """

    dt_utc = dt.astimezone(timezone.utc)
    return dt_utc.strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z"


class GraiEncoder(JSONEncoder):
    """The default JSON encoder for Grai.

    This encoder provides default serialization for a variety of datatypes including:
    * Enums
    * Pydantic models
    * UUIDs
    * Paths
    * Datetimes & dates
    * Sets
    * etc...

    Which should be reused for compatibility purposes.

    """

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
    """Dump an object to JSON following Grai's serialization rules

    This uses the GraiEncoder to serialize objects to JSON.

    Args:
        v: The object to dump
        default: A default function to use for serialization if extra types are required.

    Returns:
        The JSON string

    """
    if default is None:
        return json.dumps(v, cls=GraiEncoder)
    else:
        return json.dumps(v, default=default, cls=GraiEncoder)


def load_json(v: str) -> Any:
    """Returns a JSON object from a string"""
    return json.loads(v)


class GraiYamlSerializer:
    """A YAML serializer for Grai

    The GraiYamlSerializer provides a simple interface for serializing and deserializing YAML files which complies with Grai's serialization rules.

    """

    @staticmethod
    def load(stream: Union[str, Path, IO]) -> Union[Dict, List[Dict]]:
        """

        Args:
            stream: The stream to load from. This can be a string, a Path, or a file-like object.

        Returns:
            Either a dictionary or a list of dictionaries depending on the input
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
        """Dump an object to YAML following Grai's serialization rules

        Args:
            item: The object to dump
            stream: The stream to dump to. If None, the result is returned as a string.

        Returns:
            The YAML string

        Raises:

        """

        prepped_data = cls.prep_data(item)
        dumper: Callable = yaml.safe_dump_all if isinstance(item, Sequence) else yaml.safe_dump

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
        """Ensures that the data is in a format compliant with Grai's serialization rules.

        Args:
            data: The data to prepare

        Returns:
            If the data is a sequence, a list of strings is returned. Otherwise, a string is returned.

        Raises:

        """
        if isinstance(data, Sequence):
            return list(load_json(dump_json(item)) for item in data)
        else:
            return load_json(dump_json(data))

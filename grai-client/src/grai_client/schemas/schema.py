from pathlib import Path
from typing import Any, Dict, Iterable, Literal, Type, Union

import yaml
from grai_schemas.schema import GraiType, Schema


def validate_file(file: Union[str, Path]) -> Iterable[GraiType]:
    with open(file) as f:
        for item in yaml.safe_load_all(f):
            yield Schema(entity=item).entity

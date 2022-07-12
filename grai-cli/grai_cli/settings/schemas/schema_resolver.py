from pathlib import Path
from typing import Dict, Type, Tuple, Callable
from grai_cli.settings.schemas.utilities import base_schema
from grai_cli.utilities.utilities import load_yaml
from schema import Schema
from grai_cli.settings.schemas.node import node_versions

# TODO: This is janky, need to resolve version to types independently

version_resolvers: Dict[str, Dict[str, Callable[[], Schema]]] = {
    "Node": node_versions
}


def validate_file(file: str | Path) -> Dict:
    schema = base_schema()
    configuration = load_yaml(file)
    result: (str, str) = schema.validate(configuration)
    schema = version_resolvers[result['type']][result['version']]()
    return [schema.validate(configuration)]

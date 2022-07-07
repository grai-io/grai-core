from schema import Optional
from typing import Dict, Type, Callable
from schema import Schema


def node_schema_v1():
    from grai_cli import config

    version_fields = {

    }
    node_fields = {
        "name": str,
        Optional("namespace", default=config['context']['namespace'].get()): str,
        "data_source": str,
        Optional("display_name"): str,
        Optional("is_active"): bool,
        Optional("metadata"): dict,
    }

    node_values = {
        "spec": node_fields
    }

    schema = version_fields | node_values
    return Schema(schema, ignore_extra_keys=True)


node_versions: Dict[str, Callable[[], Schema]] = {
    "v1": node_schema_v1
}

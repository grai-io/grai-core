from typing import Dict, Literal

from dbt_artifacts_parser.parsers.manifest.manifest_v5 import ParsedSourceDefinition

from grai_source_dbt.adapters.adapters import build_app_metadata


@build_app_metadata.register
def build_metadata_from_node(current: ParsedSourceDefinition, version: Literal["v1"] = "v1") -> Dict:
    """

    Args:
        current (ParsedSourceDefinition):
        version (Literal["v1"], optional):  (Default value = "v1")

    Returns:

    Raises:

    """
    data = {
        "description": current.description,
        "dbt_resource_type": current.resource_type,
        "table_name": current.name,
        "dbt_model_name": current.unique_id,
    }

    return data

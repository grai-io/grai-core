from typing import Union

from pydantic import Extra

from grai_source_dbt.versions.v5 import V5NodeTypes, full_name

NodeTypes = V5NodeTypes

for node_type in NodeTypes.__args__:
    node_type.Config.extras = Extra.allow

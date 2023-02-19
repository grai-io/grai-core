from typing import Union

from pydantic import Extra

from grai_source_dbt.versions import base, utils, v5

SUPPORTED_VERSIONS = ["v5"]

for node_type in utils.DbtTypes.all.__args__:
    node_type.Config.extras = Extra.allow

NodeTypes = utils.DbtTypes.nodes
AllTypes = utils.DbtTypes.all

from typing import Union

from dbt_artifacts_parser.parsers.manifest.manifest_v8 import (
    AnalysisNode,
    GenericTestNode,
    HookNode,
    ModelNode,
    RPCNode,
    SeedNode,
    SingularTestNode,
    SnapshotNode,
    SourceDefinition,
    SqlNode,
)

NodeTypes = Union[
    AnalysisNode,
    SingularTestNode,
    HookNode,
    ModelNode,
    RPCNode,
    SqlNode,
    GenericTestNode,
    SnapshotNode,
    SeedNode,
]

SourceTypes = SourceDefinition

from pydantic import Extra

for obj in NodeTypes.__args__:
    obj.Config.extra = Extra.allow

SourceTypes.Config.extra = Extra.allow

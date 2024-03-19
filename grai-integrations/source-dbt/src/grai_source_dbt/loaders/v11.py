from typing import Union, get_args

from dbt_artifacts_parser.parsers.manifest.manifest_v11 import (
    AnalysisNode,
    GenericTestNode,
    HookNode,
    ManifestV11,
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

SourceTypes = Union[SourceDefinition]

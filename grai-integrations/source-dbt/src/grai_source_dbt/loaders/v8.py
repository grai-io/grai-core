from typing import Union, get_args

from dbt_artifacts_parser.parsers.manifest.manifest_v8 import (
    AnalysisNode,
    GenericTestNode,
    HookNode,
    ManifestV8,
    ModelNode,
    RPCNode,
    SeedNode,
    SingularTestNode,
    SnapshotNode,
    SourceDefinition,
    SqlNode,
)

from grai_source_dbt.utils import set_extra_fields

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

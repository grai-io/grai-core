from typing import Union, get_args

from dbt_artifacts_parser.parsers.manifest.manifest_v6 import (
    CompiledAnalysisNode,
    CompiledGenericTestNode,
    CompiledHookNode,
    CompiledModelNode,
    CompiledRPCNode,
    CompiledSeedNode,
    CompiledSingularTestNode,
    CompiledSnapshotNode,
    CompiledSqlNode,
    ManifestV6,
    ParsedAnalysisNode,
    ParsedGenericTestNode,
    ParsedHookNode,
    ParsedModelNode,
    ParsedRPCNode,
    ParsedSeedNode,
    ParsedSingularTestNode,
    ParsedSnapshotNode,
    ParsedSourceDefinition,
    ParsedSqlNode,
)

from grai_source_dbt.utils import set_extra_fields

NodeTypes = Union[
    CompiledAnalysisNode,
    CompiledSingularTestNode,
    CompiledModelNode,
    CompiledHookNode,
    CompiledRPCNode,
    CompiledSqlNode,
    CompiledGenericTestNode,
    CompiledSeedNode,
    CompiledSnapshotNode,
    ParsedAnalysisNode,
    ParsedSingularTestNode,
    ParsedHookNode,
    ParsedModelNode,
    ParsedRPCNode,
    ParsedSqlNode,
    ParsedGenericTestNode,
    ParsedSeedNode,
    ParsedSnapshotNode,
]
SourceTypes = Union[ParsedSourceDefinition]
set_extra_fields([*get_args(NodeTypes), SourceTypes])  # type: ignore

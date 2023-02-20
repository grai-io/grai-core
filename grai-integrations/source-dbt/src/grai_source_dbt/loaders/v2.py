from typing import Union, get_args

from dbt_artifacts_parser.parsers.manifest.manifest_v2 import (
    CompiledAnalysisNode,
    CompiledDataTestNode,
    CompiledHookNode,
    CompiledModelNode,
    CompiledRPCNode,
    CompiledSchemaTestNode,
    CompiledSeedNode,
    CompiledSnapshotNode,
    ManifestV2,
    ParsedAnalysisNode,
    ParsedDataTestNode,
    ParsedHookNode,
    ParsedModelNode,
    ParsedRPCNode,
    ParsedSchemaTestNode,
    ParsedSeedNode,
    ParsedSnapshotNode,
    ParsedSourceDefinition,
)

from grai_source_dbt.utils import set_extra_fields

NodeTypes = Union[
    CompiledAnalysisNode,
    CompiledDataTestNode,
    CompiledModelNode,
    CompiledHookNode,
    CompiledRPCNode,
    CompiledSchemaTestNode,
    CompiledSeedNode,
    CompiledSnapshotNode,
    ParsedAnalysisNode,
    ParsedDataTestNode,
    ParsedHookNode,
    ParsedModelNode,
    ParsedRPCNode,
    ParsedSchemaTestNode,
    ParsedSeedNode,
    ParsedSnapshotNode,
    ParsedSnapshotNode,
]
SourceTypes = Union[ParsedSourceDefinition]

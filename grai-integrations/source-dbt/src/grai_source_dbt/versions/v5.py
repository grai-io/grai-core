from typing import Any, Dict, Iterator, Sequence, Union

from dbt_artifacts_parser.parsers.manifest.manifest_v5 import (
    CompiledAnalysisNode,
    CompiledGenericTestNode,
    CompiledHookNode,
    CompiledModelNode,
    CompiledRPCNode,
    CompiledSeedNode,
    CompiledSingularTestNode,
    CompiledSnapshotNode,
    CompiledSqlNode,
    ManifestV5,
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
from multimethod import multimethod
from pydantic import BaseModel, Extra

V5NodeTypes = Union[
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


needed_v5_objs = [
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
    ParsedSourceDefinition,
]

for obj in needed_v5_objs:
    obj.Config.extra = Extra.allow


class GraiExtras(BaseModel):
    namespace: str
    full_name: str


@multimethod
def full_name(obj):
    return obj.full_name


@full_name.register
def node_full_name(obj: V5NodeTypes):
    return f"{obj.schema_}.{obj.name}"


@full_name.register
def source_full_name(obj: ParsedSourceDefinition):
    return f"{obj.schema_}.{obj.identifier}"


class NodeAttributeMixins:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @property
    def full_name(self):
        return full_name(self)


class GraiParsedAnalysisNode(NodeAttributeMixins, ParsedAnalysisNode):
    pass


class GraiCompiledSingularTestNode(NodeAttributeMixins, CompiledSingularTestNode):
    pass


class GraiCompiledModelNode(NodeAttributeMixins, CompiledModelNode):
    pass


class GraiCompiledHookNode(NodeAttributeMixins, CompiledHookNode):
    pass


class GraiCompiledRPCNode(NodeAttributeMixins, CompiledRPCNode):
    pass


class GraiCompiledSqlNode(NodeAttributeMixins, CompiledSqlNode):
    pass


class GraiCompiledGenericTestNode(NodeAttributeMixins, CompiledGenericTestNode):
    pass


class GraiCompiledSeedNode(NodeAttributeMixins, CompiledSeedNode):
    pass


class GraiCompiledSnapshotNode(NodeAttributeMixins, CompiledSnapshotNode):
    pass


class GraiParsedAnalysisNode(NodeAttributeMixins, ParsedAnalysisNode):
    pass


class GraiParsedSingularTestNode(NodeAttributeMixins, ParsedSingularTestNode):
    pass


class GraiParsedHookNode(NodeAttributeMixins, ParsedHookNode):
    pass


class GraiParsedModelNode(NodeAttributeMixins, ParsedModelNode):
    pass


class GraiParsedRPCNode(NodeAttributeMixins, ParsedRPCNode):
    pass


class GraiParsedSqlNode(NodeAttributeMixins, ParsedSqlNode):
    pass


class GraiParsedGenericTestNode(NodeAttributeMixins, ParsedGenericTestNode):
    pass


class GraiParsedSeedNode(NodeAttributeMixins, ParsedSeedNode):
    pass


class GraiParsedSnapshotNode(NodeAttributeMixins, ParsedSnapshotNode):
    pass


class GraiParsedSourceDefinition(NodeAttributeMixins, ParsedSourceDefinition):
    pass


class GraiManifestV5(ManifestV5):
    pass

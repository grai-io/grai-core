from typing import Union, get_args
from grai_source_dbt.loaders.v1 import ManifestLoaderV1
from grai_source_dbt.models.grai import Edge, EdgeTerminus
from grai_source_dbt.utils import full_name

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

SourceTypes = SourceDefinition

class ManifestLoaderV8(ManifestLoaderV1):
    def make_edge(self, source, destination, constraint_type, definition: bool = False) -> Edge:
        source_terminus = EdgeTerminus(name=full_name(source), namespace=self.namespace)
        destination_terminus = EdgeTerminus(name=full_name(destination), namespace=self.namespace)
        if definition:
            return Edge(
                constraint_type=constraint_type,
                source=source_terminus,
                destination=destination_terminus,
                # definition=source.raw_code,
            )
        else:
            return Edge(
                constraint_type=constraint_type,
                source=source_terminus,
                destination=destination_terminus,
            )
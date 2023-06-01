from typing import Optional, Union, get_args

from dbt_artifacts_parser.parsers.manifest.manifest_v7 import (
    CompiledAnalysisNode,
    CompiledGenericTestNode,
    CompiledHookNode,
    CompiledModelNode,
    CompiledRPCNode,
    CompiledSeedNode,
    CompiledSingularTestNode,
    CompiledSnapshotNode,
    CompiledSqlNode,
    ManifestV7,
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

from grai_source_dbt.loaders.v1 import ManifestLoaderV1
from grai_source_dbt.models.grai import Edge, EdgeTerminus
from grai_source_dbt.utils import full_name, set_extra_fields

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


class ManifestLoaderV7(ManifestLoaderV1):
    """ """

    def make_edge(self, source, destination, constraint_type, edge_type, definition: bool = False) -> Edge:
        """

        Args:
            source:
            destination:
            constraint_type:
            edge_type:
            definition (bool, optional):  (Default value = False)

        Returns:

        Raises:

        """
        source_terminus = EdgeTerminus(name=full_name(source), namespace=self.namespace)
        destination_terminus = EdgeTerminus(name=full_name(destination), namespace=self.namespace)
        if definition:
            return Edge(
                constraint_type=constraint_type,
                source=source_terminus,
                destination=destination_terminus,
                definition=destination.compiled_code if hasattr(destination, "compiled_code") else destination.raw_code,
                edge_type=edge_type,
            )
        else:
            return Edge(
                constraint_type=constraint_type,
                source=source_terminus,
                destination=destination_terminus,
                edge_type=edge_type,
            )

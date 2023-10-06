import json
from functools import cached_property
from typing import List, Set, Tuple, Union

from grai_schemas.v1 import SourcedEdgeV1, SourcedNodeV1
from grai_schemas.v1.source import SourceSpec

from grai_source_openlineage.adapters import adapt_to_client
from grai_source_openlineage.models import Column, Constraint, Edge, NodeTypes, Table


class OpenLineageProcessor:
    source: SourceSpec

    def __init__(self, lineage: dict, namespace: str, source: SourceSpec):
        self.lineage = lineage
        self.namespace = namespace
        self.source = source

    @cached_property
    def adapted_nodes(self) -> List[SourcedNodeV1]:
        """

        Args:

        Returns:

        Raises:

        """
        return adapt_to_client(self.nodes, self.source, "v1")

    @cached_property
    def adapted_edges(self) -> List[SourcedEdgeV1]:
        """

        Args:

        Returns:

        Raises:

        """
        return adapt_to_client(self.edges, self.source, "v1")

    @property
    def nodes(self) -> List[NodeTypes]:
        """

        Args:

        Returns:

        Raises:

        """
        nodes, edges = self.manifest

        return nodes

    @property
    def edges(self) -> List[Edge]:
        """

        Args:

        Returns:

        Raises:

        """
        nodes, edges = self.manifest

        return edges

    @cached_property
    def manifest(self) -> Tuple[List[NodeTypes], List[Edge]]:
        tables: Set[Table] = set()
        columns: Set[Column] = set()
        edges: List[Edge] = []

        outputs = self.lineage.get("outputs", [])

        for output in outputs:
            facets = output.get("facets")

            if not facets:
                continue

            output_name = output.get("name")
            output_namespace = output.get("namespace")

            table = Table(name=output_name, namespace=output_namespace)
            tables.add(table)

            fields = facets.get("columnLineage", {}).get("fields", {})

            for column_name, field in fields.items():
                column_full_name = f"{output_name}.{column_name}"
                column = Column(
                    namespace=output_namespace,
                    name=column_full_name,
                    table_name=output_name,
                )
                columns.add(column)
                edges.append(
                    Edge(
                        source=table,
                        destination=column,
                        constraint_type=Constraint("bt"),
                    )
                )

                for input_field in field.get("inputFields", []):
                    namespace = input_field["namespace"]
                    name = input_field["name"]
                    field = input_field["field"]
                    input_column_full_name = f"{name}.{field}"

                    input_table = Table(name=name, namespace=namespace)
                    tables.add(input_table)
                    input_column = Column(
                        namespace=namespace,
                        name=input_column_full_name,
                        table_name=name,
                    )
                    columns.add(input_column)
                edges.append(
                    Edge(
                        source=input_table,
                        destination=input_column,
                        constraint_type=Constraint("bt"),
                    )
                )
                edges.append(
                    Edge(
                        source=input_column,
                        destination=column,
                        constraint_type=Constraint("f"),
                    )
                )

        nodes = list(tables) + list(columns)

        return nodes, edges

    @classmethod
    def load(cls, lineage_data: Union[str, dict], namespace: str, source: SourceSpec) -> "OpenLineageProcessor":
        """

        Args:
            lineage_data:
            namespace:
            source:

        Returns:

        Raises:

        """
        if isinstance(lineage_data, str):
            lineage = json.load(lineage_data)
        else:
            lineage = lineage_data

        return OpenLineageProcessor(lineage, namespace, source)

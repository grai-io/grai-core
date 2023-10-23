from grai_source_openlineage.processor import OpenLineageProcessor


class TestOpenLineageProcessor:
    @staticmethod
    def test_processing_event(openlineage_test_event, mock_source):
        processor = OpenLineageProcessor(
            lineage=openlineage_test_event,
            source=mock_source.spec,
            namespace="default",
            namespaces={},
        )

        assert processor.source == mock_source.spec
        assert processor.namespace == "default"
        assert processor.namespaces == {}
        assert processor.lineage == openlineage_test_event

        assert len(processor.adapted_nodes) == 1

        assert processor.adapted_nodes[0].type == "SourceNode"
        assert processor.adapted_nodes[0].version == "v1"
        assert processor.adapted_nodes[0].spec.is_active is True
        assert processor.adapted_nodes[0].spec.display_name == "workshop.public.taxes-out"
        assert processor.adapted_nodes[0].spec.workspace is None

        assert processor.adapted_edges == []

    @staticmethod
    def test_processing_full_event(openlineage_test_full_event, mock_source):
        processor = OpenLineageProcessor(
            lineage=openlineage_test_full_event,
            source=mock_source.spec,
            namespace="default",
            namespaces={},
        )

        assert processor.source == mock_source.spec
        assert processor.namespace == "default"
        assert processor.namespaces == {}
        assert processor.lineage == openlineage_test_full_event

        assert len(processor.adapted_nodes) == 5
        assert len(processor.adapted_edges) == 6


def test_column_facet(test_data_getter):
    test_data_getter.get("ColumnLineageDatasetFacet")

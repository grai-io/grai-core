import os

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


def test_column_facet(test_data_getter):
    test_data_getter.get("ColumnLineageDatasetFacet")

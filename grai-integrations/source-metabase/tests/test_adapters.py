import pytest
from grai_schemas import config as core_config
from grai_schemas.v1 import EdgeV1, NodeV1, SourcedEdgeV1, SourcedNodeV1
from grai_schemas.v1.metadata import GraiEdgeMetadataV1, GraiNodeMetadataV1

from grai_source_metabase.adapters import adapt_to_client
from grai_source_metabase.models import Edge, Question, Table
from grai_source_metabase.package_definitions import config


def mock_edge_values(source, destination):
    return Edge(
        source=source,
        destination=destination,
        definition="test_definition",
        constraint_type="bt",
    )


class AdapterTestValues:
    tables = [
        Table(
            id=1,
            db_id=1,
            name="test_table",
            display_name="test_table",
            schema_name="test_schema",
            description="test_description",
            entity_type="entity/UserTable",
            namespace="test_namespace",
            db={"id": 1, "name": "test_database", "engine": "postgres"},
        )
    ]

    questions = [
        Question(
            id=1,
            name="test_question",
            description="test_description",
            result_metadata=[{"columns": [{"name": "test_column"}]}],
            creator={"id": 1, "first_name": "test", "last_name": "tester"},
            database_id=5,
            table_id=1,
            collection={"id": 1, "name": "test_collection"},
            public_uuid="test_uuid",
            namespace="test_namespace",
        )
    ]

    edges = [mock_edge_values(tables[0], questions[0])]


@pytest.mark.parametrize("item, version, target", [(item, "v1", SourcedNodeV1) for item in AdapterTestValues.tables])
def test_table_adapter(item, version, target, mock_source):
    """

    Args:
        item:
        version:
        target:

    Returns:

    Raises:

    """
    result = adapt_to_client(item, mock_source, version)
    assert isinstance(result, target)


@pytest.mark.parametrize(
    "item, version, target",
    [(item, "v1", SourcedNodeV1) for item in AdapterTestValues.questions],
)
def test_question_adapter(item, version, target, mock_source):
    """

    Args:
        item:
        version:
        target:

    Returns:

    Raises:

    """
    result = adapt_to_client(item, mock_source, version)
    assert isinstance(result, target)


@pytest.mark.parametrize("item,version,target", [(item, "v1", SourcedEdgeV1) for item in AdapterTestValues.edges])
def test_edge_adapter(item, version, target, mock_source):
    """

    Args:
        item:
        version:
        target:

    Returns:

    Raises:

    """
    result = adapt_to_client(item, mock_source, version)
    assert isinstance(result, target)


# def test_node_metadata_has_core_metadata_ids(nodes):
#     """
#
#     Args:
#         nodes:
#
#     Returns:
#
#     Raises:
#
#     """
#     for node in nodes:
#         assert hasattr(node.spec.metadata, core_config.metadata_id)
#
#
# def test_edge_metadata_has_core_metadata_ids(edges):
#     """
#
#     Args:
#         edges:
#
#     Returns:
#
#     Raises:
#
#     """
#     for edge in edges:
#         assert hasattr(edge.spec.metadata, core_config.metadata_id)
#
#
# def test_node_metadata_has_app_metadata_id(nodes):
#     """
#
#     Args:
#         nodes:
#
#     Returns:
#
#     Raises:
#
#     """
#     for node in nodes:
#         assert hasattr(node.spec.metadata, config.metadata_id)
#
#
# def test_edge_metadata_has_app_metadata_id(edges):
#     """
#
#     Args:
#         edges:
#
#     Returns:
#
#     Raises:
#
#     """
#     for edge in edges:
#         assert hasattr(edge.spec.metadata, config.metadata_id)
#
#
# def test_node_metadata_is_core_compliant(nodes):
#     """
#
#     Args:
#         nodes:
#
#     Returns:
#
#     Raises:
#
#     """
#     for node in nodes:
#         assert isinstance(getattr(node.spec.metadata, core_config.metadata_id), GraiNodeMetadataV1)
#
#
# def test_edge_metadata_is_core_compliant(edges):
#     """
#
#     Args:
#         edges:
#
#     Returns:
#
#     Raises:
#
#     """
#     for edge in edges:
#         assert isinstance(getattr(edge.spec.metadata, core_config.metadata_id), GraiEdgeMetadataV1)

import pytest
from grai_schemas import config as core_config
from grai_schemas.v1 import SourcedEdgeV1, SourcedNodeV1
from grai_schemas.v1.metadata import GraiEdgeMetadataV1, GraiNodeMetadataV1

from grai_source_looker.adapters import adapt_to_client
from grai_source_looker.models import (
    Constraint,
    Dashboard,
    Dimension,
    Edge,
    Explore,
    Query,
)
from grai_source_looker.package_definitions import config


def mock_edge_values():
    """ """
    extra_args = {
        "is_primary_key": True,
        "is_foreign_key": False,
        "fivetran_id": "abc",
        "fivetran_table_id": "123",
    }
    source = Dashboard(
        id="test", title="test", table_schema="schema", table_name="table", name="id", namespace="test", **extra_args
    )
    destination = Query(
        id=1,
        model="test",
        view="test",
        fields=["field1"],
        table_schema="schema",
        table_name="table",
        name="id2",
        namespace="test",
        **extra_args
    )

    return []

    test_edges = [
        Edge(
            name="test",
            source=source,
            destination=destination,
            definition="thing",
            constraint_type=Constraint("bt"),
        )
    ]
    return test_edges


class AdapterTestValues:
    """ """

    dashboards = [
        Dashboard(
            id="test",
            title="test",
            name="test",
            namespace="tests",
            table_name="test",
            table_schema="test",
            is_primary_key=True,
            is_foreign_key=False,
            fivetran_id="easyas",
            fivetran_table_id="abc123",
        )
    ]

    queries = [
        Query(
            id=1,
            model="test",
            view="test",
            fields=["field1"],
            name="test",
            namespace="tests",
            schema_name="test",
            fivetran_id="test",
        )
    ]

    dimension = Dimension(name="test", label="test", type="test", sql="test")

    explores = [
        Explore(
            id="test",
            name="test",
            fields={"dimensions": [dimension]},
            sql_table_name="test",
        )
    ]

    dimensions = [dimension]

    edges = mock_edge_values()


@pytest.mark.parametrize(
    "item,version,target",
    [(item, "v1", SourcedNodeV1) for item in AdapterTestValues.dashboards],
)
def test_dashboard_adapter(item, version, target, mock_source):
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
    "item,version,target",
    [(item, "v1", SourcedNodeV1) for item in AdapterTestValues.queries],
)
def test_query_adapter(item, version, target, mock_source):
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
    "item,version,target",
    [(item, "v1", SourcedNodeV1) for item in AdapterTestValues.explores],
)
def test_explore_adapter(item, version, target, mock_source):
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
    "item,version,target",
    [(item, "v1", SourcedNodeV1) for item in AdapterTestValues.dimensions],
)
def test_dimension_adapter(item, version, target, mock_source):
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
    "item,version,target",
    [(item, "v1", SourcedEdgeV1) for item in AdapterTestValues.edges],
)
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

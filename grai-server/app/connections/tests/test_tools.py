import pytest
from grai_schemas.v1 import NodeV1
from grai_schemas.v1.metadata.nodes import (
    ColumnAttributes,
    ColumnMetadata,
    NodeTypeLabels,
)

from connections.adapters.tools import NullableTestResult


@pytest.fixture
def test_node_v1():
    metadata = ColumnAttributes(is_nullable=False, is_unique=False, data_type="String")
    column_metadata = ColumnMetadata(node_type=NodeTypeLabels.column.value, node_attributes=metadata)

    return NodeV1.from_spec(
        {
            "name": "node1",
            "namespace": "default",
            "data_source": "test",
            "display_name": "node1",
            "metadata": {"grai": column_metadata.dict()},
        }
    )


@pytest.mark.django_db
def test_nullable_test_result(test_node_v1):
    result = NullableTestResult(test_node_v1, [test_node_v1])

    assert result.type == "Nullable"
    assert result.test_pass == False


@pytest.mark.django_db
def test_test_result_to_json(test_node_v1):
    result = NullableTestResult(test_node_v1, [test_node_v1])

    dict = result.toJSON()

    assert dict["type"] == "Nullable"
    assert dict["test_pass"] == False

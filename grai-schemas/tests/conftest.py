import pytest
from grai_schemas.v1.mock import MockV1


@pytest.fixture
def mock_v1():
    return MockV1()

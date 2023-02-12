import pytest
from grai_source_fivetran.loader import FivetranConnector, FivetranGraiMapper


# You may need to create a .env file to run these tests
@pytest.fixture
def connector():
    return FivetranConnector()


@pytest.fixture
def mapper():
    return FivetranGraiMapper()

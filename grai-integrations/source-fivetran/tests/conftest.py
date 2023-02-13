import pytest
from dotenv import load_dotenv
from grai_source_fivetran.loader import FivetranConnector, FivetranGraiMapper


# You may need to create a .env file to run these tests
@pytest.fixture
def connector():
    return FivetranConnector()


@pytest.fixture
def mapper():
    load_dotenv()
    return FivetranGraiMapper(default_namespace="default")


@pytest.fixture
def mapped_nodes_and_edges(mapper):
    return mapper.get_nodes_and_edges()


@pytest.fixture
def nodes(mapped_nodes_and_edges):
    return mapped_nodes_and_edges[0]


@pytest.fixture
def edges(mapped_nodes_and_edges):
    return mapped_nodes_and_edges[1]

import pytest

from grai_client.utilities.tests import get_test_client


@pytest.fixture
def client():
    return get_test_client()

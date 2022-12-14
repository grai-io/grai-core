import pytest

from grai_client.update import update
from grai_client.utilities.tests import get_test_client

clients = [get_test_client()]


@pytest.mark.parametrize("client", clients)
def test_update_no_updates(client):
    result = update(client, [])
    assert result is None

from unittest.mock import MagicMock

import pytest

from api.search import Search


@pytest.mark.django_db
async def test_workspace_search_key(mocker):
    mock = mocker.patch("api.search.SearchClient.generate_secured_api_key")
    search_client = "search_key"
    mock.return_value = search_client

    client = Search()

    search_key = client.generate_secured_api_key("search_key", {"filters": "workspace_id:1"})

    assert search_key == "search_key"

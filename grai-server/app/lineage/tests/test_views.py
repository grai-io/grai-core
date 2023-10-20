from itertools import product

import pytest
from django.urls import reverse

from lineage.urls import app_name

actions = ["list"]
route_prefixes = ["nodes", "edges", "sources"]
targets = [(f"{app_name}:{prefix}-{action}", 200) for prefix, action in product(route_prefixes, actions)]


@pytest.mark.parametrize("url_name,status", targets)
@pytest.mark.django_db
def test_get_endpoints(auto_login_user, url_name, status):
    client, user = auto_login_user()
    url = reverse(url_name)
    response = client.get(url)
    assert response.status_code == status, f"verb `get` failed on {url} with status {response.status_code}"

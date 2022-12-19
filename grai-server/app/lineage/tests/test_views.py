import json
import uuid
from itertools import product

import django.db.utils
import pytest
from django.test import Client
from django.test.client import RequestFactory
from django.urls import reverse
from lineage.models import Edge, Node
from lineage.urls import app_name
from rest_framework.test import APIClient, force_authenticate
from rest_framework_api_key.models import APIKey
from users.models import User
from workspaces.models import Workspace, WorkspaceAPIKey, Membership


def create_node(client, workspace, name=None, namespace="default", data_source="test"):
    args = {
        "name": uuid.uuid4() if name is None else name,
        "namespace": namespace,
        "data_source": data_source,
        "workspace": str(workspace.id),
    }

    url = reverse("graph:nodes-list")
    response = client.post(url, args, SERVER_NAME="localhost")
    return response


def create_edge(
    client, workspace, source=None, destination=None, data_source="test", **kwargs
):
    if source is None:
        source = create_node(client, workspace).json()["id"]
    if destination is None:
        destination = create_node(client, workspace).json()["id"]
    args = {
        "data_source": data_source,
        "source": source,
        "destination": destination,
        "workspace": str(workspace.id),
    }

    url = reverse("graph:edges-list")
    response = client.post(url, args, **kwargs)
    return response


@pytest.fixture
def test_password():
    return "strong-test-pass"


def get_username():
    return f"{str(uuid.uuid4())}@gmail.com"


@pytest.fixture
def create_user(db, django_user_model, test_password):
    def make_user(**kwargs):
        kwargs["password"] = test_password
        kwargs.setdefault("username", get_username())
        return django_user_model.objects.create_user(**kwargs)

    return make_user


@pytest.fixture
def auto_login_user(db, client, create_user, test_password):
    def make_auto_login(user=None):
        if user is None:
            user = create_user()
            client.login(username=user.username, password=test_password)
        return client, user

    return make_auto_login


actions = ["list"]
route_prefixes = ["nodes", "edges"]
targets = [
    (f"{app_name}:{prefix}-{action}", 200)
    for prefix, action in product(route_prefixes, actions)
]


# @pytest.mark.parametrize("url_name,status", targets)
# @pytest.mark.django_db
# def test_get_endpoints(auto_login_user, url_name, status):
#     client, user = auto_login_user()
#     url = reverse(url_name)
#     response = client.get(url)
#     assert response.status_code == status


# @pytest.mark.django_db
# def test_post_node(api_key, test_workspace):
#     client = APIClient()
#     client.credentials(HTTP_AUTHORIZATION=f"Api-Key {api_key}")
#     response = create_node(client, test_workspace)
#     assert response.status_code == 201


# @pytest.mark.django_db
# def test_patch_node(api_key, test_workspace):
#     client = APIClient()
#     client.credentials(HTTP_AUTHORIZATION=f"Api-Key {api_key}")
#     response = create_node(client, test_workspace)
#     assert response.status_code == 201
#     node_id = response.json()["id"]

#     url = reverse("graph:nodes-detail", kwargs={"pk": node_id})
#     args = {
#         "namespace": "string",
#         "name": "strisdfsdfng",
#         "display_name": "string",
#         "data_source": "string",
#         "metadata": {
#             "additionalProp1": "string",
#             "additionalProp2": "string",
#             "additionalProp3": "string",
#         },
#         "is_active": False,
#     }
#     result = client.patch(url, json.dumps(args), content_type="application/json")
#     assert result.status_code == 200
#     result = result.json()
#     assert all(result[key] == value for key, value in args.items())


# @pytest.mark.django_db
# def test_delete_node(api_key, test_workspace):
#     client = APIClient()
#     client.credentials(HTTP_AUTHORIZATION=f"Api-Key {api_key}")
#     response = create_node(client, test_workspace)
#     assert response.status_code == 201
#     node_id = response.json()["id"]

#     url = reverse("graph:nodes-detail", kwargs={"pk": node_id})
#     result = client.delete(url)
#     assert result.status_code == 204

#     result = client.get(reverse("graph:nodes-detail", kwargs={"pk": node_id}))
#     assert result.status_code == 404


# @pytest.mark.django_db
# def test_post_edge(api_key, test_workspace):
#     client = APIClient()
#     client.credentials(HTTP_AUTHORIZATION=f"Api-Key {api_key}")
#     response = create_edge(client, test_workspace)
#     assert response.status_code == 201


# @pytest.mark.django_db
# def test_duplicate_nodes(api_key, test_workspace):
#     client = APIClient()
#     client.credentials(HTTP_AUTHORIZATION=f"Api-Key {api_key}")
#     name = "test_node"
#     create_node(client, test_workspace, name)
#     with pytest.raises(django.db.utils.IntegrityError):
#         response = create_node(client, test_workspace, name)


# @pytest.mark.django_db
# def test_duplicate_edge_nodes(api_key, test_workspace):
#     client = APIClient()
#     client.credentials(HTTP_AUTHORIZATION=f"Api-Key {api_key}")
#     node_id = create_node(client, test_workspace).json()["id"]
#     with pytest.raises(django.db.utils.IntegrityError):
#         response = create_edge(
#             client, test_workspace, source=node_id, destination=node_id
#         )


@pytest.fixture
def test_workspace(name=None):
    return Workspace.objects.create(name=uuid.uuid4() if name is None else name)


@pytest.fixture
def test_membership(user):
    return Membership.objects.create(role="admin", user=user, workspace=test_workspace)


@pytest.fixture
def api_key(create_user, test_workspace):
    user = create_user()
    api_key, key = WorkspaceAPIKey.objects.create_key(
        name="ContentAP-tests", workspace=test_workspace, created_by=user
    )
    return key


@pytest.mark.django_db
def test_password_auth(db, create_user, test_password, test_workspace):
    client = APIClient()
    user = create_user()
    client.force_login(user=user)
    response = create_node(client, test_workspace)
    assert response.status_code == 201


@pytest.mark.django_db
def test_incorrect_password_auth(db, client, create_user, test_workspace):
    user = create_user()
    client.login(username=user.username, password="wrong_password")
    response = create_node(client, test_workspace)
    assert response.status_code == 403


@pytest.mark.django_db
def test_no_auth(db, client, create_user, test_workspace):
    client.logout()
    response = create_node(client, test_workspace)
    assert response.status_code == 403


@pytest.mark.django_db
def test_password_auth2(db, create_user, test_password, test_workspace):
    client = APIClient()
    user = create_user()
    client.force_login(user=user)
    response = create_node(client, test_workspace)
    assert response.status_code == 201


@pytest.mark.django_db
def test_api_key_auth(api_key, test_workspace):
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION=f"Api-Key {api_key}")
    response = create_node(client, test_workspace)
    assert response.status_code == 201
    client.credentials()
    client.logout()


@pytest.mark.django_db
def test_password_auth3(db, create_user, test_password, test_workspace):
    client = APIClient()
    user = create_user()
    client.force_login(user=user)
    response = create_node(client, test_workspace)
    assert response.status_code == 201


@pytest.mark.django_db
def test_invalid_api_key_auth(db, create_user, api_key, test_workspace):
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION=f"Api-Key wrong_api_key")
    response = create_node(client, test_workspace)
    assert response.status_code == 403


@pytest.fixture
def test_nodes(db, api_key, test_workspace, n=2):
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION=f"Api-Key {api_key}")
    nodes = [create_node(client, test_workspace).json()["id"] for i in range(n)]
    return nodes


@pytest.mark.django_db
def test_password_auth4(db, create_user, test_password, test_workspace):
    client = APIClient()
    user = create_user()
    client.force_login(user=user)
    response = create_node(client, test_workspace)
    assert response.status_code == 201


@pytest.mark.django_db
def test_incorrect_password_auth2(db, client, create_user, test_workspace, test_nodes):
    user = create_user()
    client.logout()
    client.login(username=user.username, password="wrong_password")
    response = create_edge(client, test_workspace, *test_nodes)
    assert response.status_code == 403


@pytest.mark.django_db
def test_no_auth2(db, client, create_user, test_nodes, test_workspace):
    client.logout()
    response = create_edge(client, test_workspace, *test_nodes)
    assert response.status_code == 403


@pytest.mark.django_db
def test_api_key_auth2(db, api_key, test_workspace, test_nodes):
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION=f"Api-Key {api_key}")
    response = create_edge(client, test_workspace, *test_nodes)
    assert response.status_code == 201


@pytest.mark.django_db
def test_invalid_api_key_auth2(db, api_key, test_workspace, test_nodes):
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION=f"Api-Key wrong_api_key")
    response = create_edge(client, test_workspace, *test_nodes)
    assert response.status_code == 403

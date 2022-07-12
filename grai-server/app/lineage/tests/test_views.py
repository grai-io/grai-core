import uuid

import django.db.utils
import pytest
from itertools import product
from django.test import Client
from django.urls import reverse
from lineage.urls import app_name
from users.models import User
from lineage.models import Node, Edge
from django.test.client import RequestFactory
from rest_framework.test import force_authenticate
from rest_framework.test import APIClient
from rest_framework_api_key.models import APIKey


def create_node(client, name=None, namespace='default', data_source='test'):
    args = {
        'name': uuid.uuid4() if name is None else name,
        'namespace': namespace,
        'data_source': data_source,
    }

    url = reverse('graph:nodes-list')
    response = client.post(url, args)
    return response


def create_edge(client, source=None, destination=None, data_source='test', **kwargs):
    if source is None:
        source = create_node(client).json()['id']
    if destination is None:
        destination = create_node(client).json()['id']
    args = {
        'data_source': data_source,
        'source': source,
        'destination': destination
    }

    url = reverse('graph:edges-list')
    print(kwargs)
    response = client.post(url, args, **kwargs)
    return response


actions = ['list']
route_prefixes = ['nodes', 'edges']
targets = [(f'{app_name}:{prefix}-{action}', 200)
           for prefix, action in product(route_prefixes, actions)]


@pytest.fixture
def test_password():
    return 'strong-test-pass'


def test_username():
    return f'{str(uuid.uuid4())}@gmail.com'


@pytest.fixture
def create_user(db, django_user_model, test_password):
    def make_user(**kwargs):
        kwargs['password'] = test_password
        kwargs.setdefault('username', test_username())
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


@pytest.mark.parametrize("url_name,status", targets)
@pytest.mark.django_db
def test_get_endpoints(auto_login_user, url_name, status):
    client, user = auto_login_user()
    url = reverse(url_name)
    response = client.get(url)
    assert response.status_code == status


@pytest.mark.django_db
def test_post_node(auto_login_user):
    client, user = auto_login_user()
    response = create_node(client)
    assert response.status_code == 201


@pytest.mark.django_db
def test_post_edge(auto_login_user):
    client, user = auto_login_user()
    response = create_edge(client)
    assert response.status_code == 201


@pytest.mark.django_db
def test_duplicate_nodes(auto_login_user):
    client, user = auto_login_user()
    name = 'test_node'
    create_node(client, name)
    with pytest.raises(django.db.utils.IntegrityError):
        response = create_node(client, name)


@pytest.mark.django_db
def test_duplicate_edge_nodes(auto_login_user):
    client, user = auto_login_user()
    node_id = create_node(client).json()['id']
    with pytest.raises(django.db.utils.IntegrityError):
        response = create_edge(client, source=node_id, destination=node_id)


@pytest.fixture
def api_key():
    api_key, key = APIKey.objects.create_key(name=str(uuid.uuid4()))
    return key


class TestNodeUserAuth:
    def test_password_auth(self, db, client, create_user, test_password):
        user = create_user()
        client.login(username=user.username, password=test_password)
        response = create_node(client)
        assert response.status_code == 201

    def test_incorrect_password_auth(self, db, client, create_user):
        user = create_user()
        client.login(username=user.username, password='wrong_password')
        response = create_node(client)
        assert response.status_code == 403

    def test_no_auth(self, db, client, create_user):
        user = create_user()
        response = create_node(client)
        assert response.status_code == 403

    def test_token_auth(self, db, client, create_user):
        user = create_user()
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION=f'Token {user.auth_token.key}')
        response = create_node(client)
        assert response.status_code == 201

    def test_invalid_token_auth(self, db, client, create_user):
        user = create_user()
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION=f'Token wrong_token')
        response = create_node(client)
        assert response.status_code == 403

    def test_api_key_auth(self, db, client, create_user, api_key):
        user = create_user()
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION=f'Api-Key {api_key}')
        response = create_node(client)
        assert response.status_code == 201

    def test_invalid_api_key_auth(self, db, client, create_user, api_key):
        user = create_user()
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION=f'Api-Key wrong_api_key')
        response = create_node(client)
        assert response.status_code == 403


@pytest.fixture
def test_nodes(db, client, auto_login_user, n=2):
    client, user = auto_login_user()
    nodes = [create_node(client).json()['id'] for i in range(n)]
    return nodes


class TestEdgeUserAuth:
    def test_password_auth(self, db, client, auto_login_user, test_nodes):
        client, user = auto_login_user()
        response = create_edge(client, *test_nodes)
        assert response.status_code == 201

    def test_incorrect_password_auth(self, db, client, create_user, test_nodes):
        user = create_user()
        client.logout()
        client.login(username=user.username, password='wrong_password')
        response = create_edge(client, *test_nodes)
        assert response.status_code == 403

    def test_no_auth(self, db, client, create_user, test_nodes):
        client.logout()
        response = create_edge(client, *test_nodes)
        assert response.status_code == 403

    def test_token_auth(self, db, create_user, *test_nodes):
        user = create_user()
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION=f'Token {user.auth_token.key}')
        response = create_edge(client, *test_nodes)
        assert response.status_code == 201

    def test_invalid_token_auth(self, db, create_user, test_nodes):
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION=f'Token wrong_token')
        response = create_edge(client, *test_nodes)
        assert response.status_code == 403

    def test_api_key_auth(self, db, api_key, test_nodes):
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION=f'Api-Key {api_key}')
        response = create_edge(client, *test_nodes)
        assert response.status_code == 201

    def test_invalid_api_key_auth(self, db, api_key, test_nodes):
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION=f'Api-Key wrong_api_key')
        response = create_edge(client, *test_nodes)
        assert response.status_code == 403

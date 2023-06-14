import uuid
from itertools import product

import django.db.utils
import pytest
from django.test import Client
from django.test.client import RequestFactory
from django.urls import reverse
from rest_framework.test import force_authenticate

from lineage.models import Edge, Node
from lineage.urls import app_name
from users.models import User


@pytest.fixture
def test_password():
    return "strong-test-pass"


def generate_test_username():
    return f"{str(uuid.uuid4())}@gmail.com"


@pytest.fixture
def create_user(db, django_user_model, test_password):
    def make_user(**kwargs):
        kwargs["password"] = test_password
        kwargs.setdefault("username", generate_test_username())
        return django_user_model.objects.create_user(**kwargs)

    return make_user


class TestUserAuth:
    def test_password_auth(self, db, client, create_user, test_password):
        user = create_user()
        success = client.login(username=user.username, password=test_password)
        assert success is True

    def test_password_hash_auth(self, db, client, create_user):
        user = create_user()
        success = client.login(username=user.username, password=user.password)
        assert success is False

    def test_incorrect_password_auth(self, db, client, create_user, test_password):
        user = User.objects.create_user(username="test@gmail.com", password=test_password)
        success = client.login(username=user.username, password="wrong_password")
        assert success is False

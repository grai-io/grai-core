import datetime
import types
import uuid
from unittest.mock import MagicMock

import pytest
from django_celery_beat.models import PeriodicTask

from connections.models import Connection, Connector, Run
from lineage.models import Source
from workspaces.models import Organisation, Workspace


@pytest.fixture
def test_organisation():
    organisation = Organisation.objects.create(name=str(uuid.uuid4()))

    return organisation


@pytest.fixture
def test_workspace(test_organisation):
    workspace = Workspace.objects.create(name=str(uuid.uuid4()), organisation=test_organisation)

    return workspace


@pytest.fixture
def test_source(test_workspace):
    source = Source.objects.create(name=str(uuid.uuid4()), workspace=test_workspace)

    return source


@pytest.fixture
def test_connector():
    connector = Connector.objects.create(name=str(uuid.uuid4()))

    return connector


@pytest.fixture
def test_connection(test_connector, test_workspace, test_source):
    connection = Connection.objects.create(
        workspace=test_workspace,
        connector=test_connector,
        name=str(uuid.uuid4()),
        source=test_source,
    )

    return connection


@pytest.mark.django_db
def test_connector_created():
    connector = Connector.objects.create(name="C1")

    assert connector.id == uuid.UUID(str(connector.id))
    assert str(connector) == "C1"
    assert connector.name == "C1"


@pytest.mark.django_db
def test_run_created(test_workspace, test_connection, test_source):
    run = Run.objects.create(
        workspace=test_workspace,
        connection=test_connection,
        status="success",
        source=test_source,
    )

    assert run.id == uuid.UUID(str(run.id))
    assert str(run) == str(run.id)
    assert run.status == "success"
    assert isinstance(run.metadata, dict) and len(run.metadata.keys()) == 0
    assert isinstance(run.created_at, datetime.datetime)
    assert isinstance(run.updated_at, datetime.datetime)
    assert run.started_at is None
    assert run.finished_at is None


class TestConnection:
    @pytest.mark.django_db
    def test_connection_created(self, test_workspace, test_connector, test_source):
        connection = Connection.objects.create(
            workspace=test_workspace,
            connector=test_connector,
            name="Connection 1",
            source=test_source,
        )

        assert connection.id == uuid.UUID(str(connection.id))
        assert str(connection) == "Connection 1"
        assert connection.name == "Connection 1"

    @pytest.mark.django_db
    def test_connection_updated_with_schedule(self, test_workspace, test_connector, test_source):
        connection = Connection.objects.create(
            workspace=test_workspace,
            connector=test_connector,
            name="Connection 1",
            source=test_source,
        )

        connection.schedules = {
            "type": "cron",
            "cron": {
                "minutes": "*",
                "hours": "*",
                "day_of_week": "*",
                "day_of_month": "*",
                "month_of_year": "*",
            },
        }

        connection.save()

        assert connection.id == uuid.UUID(str(connection.id))
        assert str(connection) == "Connection 1"
        assert connection.name == "Connection 1"
        assert connection.task is not None

    @pytest.mark.django_db
    def test_connection_updated_with_existing_task(self, test_workspace, test_connector, test_source):
        connection = Connection.objects.create(
            workspace=test_workspace,
            connector=test_connector,
            source=test_source,
            name="Connection 1",
            schedules={
                "type": "cron",
                "cron": {
                    "minutes": "*",
                    "hours": "*",
                    "day_of_week": "*",
                    "day_of_month": "*",
                    "month_of_year": "*",
                },
            },
        )

        connection.schedules = {
            "type": "cron",
            "cron": {
                "minutes": "30",
                "hours": "*",
                "day_of_week": "*",
                "day_of_month": "*",
                "month_of_year": "*",
            },
        }

        connection.save()

        assert connection.id == uuid.UUID(str(connection.id))
        assert str(connection) == "Connection 1"
        assert connection.name == "Connection 1"
        assert connection.task is not None

    @pytest.mark.django_db
    def test_connection_updated_with_incorrect_schedule(self, test_workspace, test_connector, test_source):
        connection = Connection.objects.create(
            workspace=test_workspace,
            connector=test_connector,
            name="Connection 1",
            source=test_source,
        )

        connection.schedules = {
            "type": "blah",
        }

        with pytest.raises(Exception) as e_info:
            connection.save()

        assert str(e_info.value) == "Schedule type not found"

    @pytest.mark.django_db
    def test_connection_updated_remove_schedule(self, test_workspace, test_connector, test_source):
        connection = Connection.objects.create(
            workspace=test_workspace,
            connector=test_connector,
            name="Connection 1",
            source=test_source,
        )

        connection.schedules = {
            "type": "cron",
            "cron": {
                "minutes": "*",
                "hours": "*",
                "day_of_week": "*",
                "day_of_month": "*",
                "month_of_year": "*",
            },
        }

        connection.save()

        assert connection.id == uuid.UUID(str(connection.id))
        assert str(connection) == "Connection 1"
        assert connection.name == "Connection 1"
        assert connection.task is not None

        task = connection.task

        connection.schedules = None
        connection.save()

        assert connection.task is None

        with pytest.raises(PeriodicTask.DoesNotExist) as e_info:
            PeriodicTask.objects.get(id=task.id)

        assert str(e_info.value) == "PeriodicTask matching query does not exist."

    @pytest.mark.django_db
    def test_connection_created_dbt_cloud(self, mocker, test_workspace, test_connector, test_source):
        hmac_secret = "74d5de51a03ccbea9936aea756b2cc044d3816de"

        mock = mocker.patch("connections.schedules.dbt_cloud.dbtCloudClient")

        dbt_cloud = types.SimpleNamespace()

        cloud = MagicMock()
        cloud.list_accounts.return_value = {"data": [{"id": 165072, "name": "test"}]}
        cloud.create_webhook.return_value = {
            "data": {
                "id": "1234webhook",
                "hmac_secret": hmac_secret,
            }
        }

        dbt_cloud.cloud = cloud

        mock.return_value = dbt_cloud

        connection = Connection.objects.create(
            workspace=test_workspace,
            connector=test_connector,
            source=test_source,
            name=str(uuid.uuid4()),
            secrets={"api_key": "1234"},
            schedules={"dbt_cloud": {"job_id": "282191"}, "type": "dbt-cloud"},
        )

        assert connection.schedules.get("dbt_cloud", {}).get("hmac_secret") == hmac_secret

    @pytest.mark.django_db
    def test_connection_updated_dbt_cloud(self, mocker, test_workspace, test_connector, test_source):
        hmac_secret = "74d5de51a03ccbea9936aea756b2cc044d3816de"

        mock = mocker.patch("connections.schedules.dbt_cloud.dbtCloudClient")

        dbt_cloud = types.SimpleNamespace()

        cloud = MagicMock()
        cloud.list_accounts.return_value = {"data": [{"id": 165072, "name": "test"}]}
        cloud.create_webhook.return_value = {
            "data": {
                "id": "1234webhook",
                "hmac_secret": hmac_secret,
            }
        }

        dbt_cloud.cloud = cloud

        mock.return_value = dbt_cloud

        connection = Connection.objects.create(
            workspace=test_workspace,
            connector=test_connector,
            source=test_source,
            name=str(uuid.uuid4()),
            secrets={"api_key": "1234"},
            schedules={"dbt_cloud": {"job_id": "282191"}, "type": "dbt-cloud"},
        )

        assert connection.schedules.get("dbt_cloud", {}).get("hmac_secret") == hmac_secret

        connection.name = "New Name"
        connection.save()

        assert connection.name == "New Name"

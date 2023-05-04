import datetime
import types
import uuid
from unittest.mock import MagicMock

import pytest
from django_celery_beat.models import PeriodicTask

from connections.models import Connection, Connector, Run
from workspaces.models import Organisation, Workspace


@pytest.mark.django_db
def test_connector_created():
    connector = Connector.objects.create(name="C1")

    assert connector.id == uuid.UUID(str(connector.id))
    assert str(connector) == "C1"
    assert connector.name == "C1"


@pytest.mark.django_db
def test_run_created():
    organisation = Organisation.objects.create(name="O1")
    workspace = Workspace.objects.create(name="W1", organisation=organisation)
    connector = Connector.objects.create(name="C1")
    connection = Connection.objects.create(workspace=workspace, connector=connector, name="Connection 1")

    run = Run.objects.create(workspace=workspace, connection=connection, status="success")

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
    def test_connection_created(self):
        organisation = Organisation.objects.create(name="O1")
        workspace = Workspace.objects.create(name="W1", organisation=organisation)
        connector = Connector.objects.create(name="C1")
        connection = Connection.objects.create(workspace=workspace, connector=connector, name="Connection 1")

        assert connection.id == uuid.UUID(str(connection.id))
        assert str(connection) == "Connection 1"
        assert connection.name == "Connection 1"

    @pytest.mark.django_db
    def test_connection_updated_with_schedule(self):
        organisation = Organisation.objects.create(name="O1")
        workspace = Workspace.objects.create(name="W1", organisation=organisation)
        connector = Connector.objects.create(name="C1")
        connection = Connection.objects.create(workspace=workspace, connector=connector, name="Connection 1")

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
    def test_connection_updated_with_existing_task(self):
        organisation = Organisation.objects.create(name="O1")
        workspace = Workspace.objects.create(name="W1", organisation=organisation)
        connector = Connector.objects.create(name="C1")
        connection = Connection.objects.create(
            workspace=workspace,
            connector=connector,
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
    def test_connection_updated_with_incorrect_schedule(self):
        organisation = Organisation.objects.create(name="O1")
        workspace = Workspace.objects.create(name="W1", organisation=organisation)
        connector = Connector.objects.create(name="C1")
        connection = Connection.objects.create(workspace=workspace, connector=connector, name="Connection 1")

        connection.schedules = {
            "type": "blah",
        }

        with pytest.raises(Exception) as e_info:
            connection.save()

        assert str(e_info.value) == "Schedule type not found"

    @pytest.mark.django_db
    def test_connection_updated_remove_schedule(self):
        organisation = Organisation.objects.create(name="O1")
        workspace = Workspace.objects.create(name="W1", organisation=organisation)
        connector = Connector.objects.create(name="C1")
        connection = Connection.objects.create(workspace=workspace, connector=connector, name="Connection 1")

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
    def test_connection_created_dbt_cloud(self, mocker):
        organisation = Organisation.objects.create(name="O1")
        workspace = Workspace.objects.create(name="W1", organisation=organisation)
        connector = Connector.objects.create(name=Connector.DBT_CLOUD, slug=Connector.DBT_CLOUD)

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
            workspace=workspace,
            connector=connector,
            name=str(uuid.uuid4()),
            secrets={"api_key": "1234"},
            schedules={"dbt_cloud": {"job_id": "282191"}, "type": "dbt-cloud"},
        )

        assert connection.schedules.get("dbt_cloud", {}).get("hmac_secret") == hmac_secret

    @pytest.mark.django_db
    def test_connection_updated_dbt_cloud(self, mocker):
        organisation = Organisation.objects.create(name="O1")
        workspace = Workspace.objects.create(name="W1", organisation=organisation)
        connector = Connector.objects.create(name=Connector.DBT_CLOUD, slug=Connector.DBT_CLOUD)

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
            workspace=workspace,
            connector=connector,
            name=str(uuid.uuid4()),
            secrets={"api_key": "1234"},
            schedules={"dbt_cloud": {"job_id": "282191"}, "type": "dbt-cloud"},
        )

        assert connection.schedules.get("dbt_cloud", {}).get("hmac_secret") == hmac_secret

        connection.name = "New Name"
        connection.save()

        assert connection.name == "New Name"

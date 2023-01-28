import datetime
import uuid

import pytest

from connections.models import Connection, Connector, Run
from workspaces.models import Workspace


@pytest.mark.django_db
def test_connector_created():
    workspace = Workspace.objects.create(name="W1")
    connector = Connector.objects.create(name="C1")

    assert connector.id == uuid.UUID(str(connector.id))
    assert str(connector) == "C1"
    assert connector.name == "C1"


@pytest.mark.django_db
def test_run_created():
    workspace = Workspace.objects.create(name="W1")
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
        workspace = Workspace.objects.create(name="W1")
        connector = Connector.objects.create(name="C1")
        connection = Connection.objects.create(workspace=workspace, connector=connector, name="Connection 1")

        assert connection.id == uuid.UUID(str(connection.id))
        assert str(connection) == "Connection 1"
        assert connection.name == "Connection 1"

    @pytest.mark.django_db
    def test_connection_updated_with_schedule(self):
        workspace = Workspace.objects.create(name="W1")
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
        workspace = Workspace.objects.create(name="W1")
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
        workspace = Workspace.objects.create(name="W1")
        connector = Connector.objects.create(name="C1")
        connection = Connection.objects.create(workspace=workspace, connector=connector, name="Connection 1")

        connection.schedules = {
            "type": "blah",
        }

        with pytest.raises(Exception) as e_info:
            connection.save()

        assert str(e_info.value) == "Schedule type not found"

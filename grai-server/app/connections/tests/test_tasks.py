import pytest
from decouple import config

from connections.models import Connection, Connector, Run
from connections.tasks import run_connection_schedule, run_update_server
from workspaces.models import Workspace


@pytest.fixture
def test_workspace():
    return Workspace.objects.create(name="W10")


@pytest.fixture
def test_postgres_connector():
    return Connector.objects.create(name="PostgreSQL")


@pytest.fixture
def test_connector():
    return Connector.objects.create(name="Connector")


@pytest.mark.django_db
class TestUpdateServer:
    def test_run_update_server_postgres(self, test_workspace, test_postgres_connector):
        connection = Connection.objects.create(
            name="C1",
            connector=test_postgres_connector,
            workspace=test_workspace,
            metadata={
                "host": config("DB_HOST", "localhost"),
                "port": 5432,
                "dbname": "grai",
                "user": "grai",
            },
            secrets={"password": "grai"},
        )
        run = Run.objects.create(connection=connection, workspace=test_workspace)

        run_update_server(str(run.id))

    def test_run_update_server_postgres_no_host(
        self, test_workspace, test_postgres_connector
    ):
        connection = Connection.objects.create(
            name="C2",
            connector=test_postgres_connector,
            workspace=test_workspace,
            metadata={"host": "a", "port": 5432, "dbname": "grai", "user": "grai"},
            secrets={"password": "grai"},
        )
        run = Run.objects.create(connection=connection, workspace=test_workspace)

        with pytest.raises(Exception) as e_info:
            run_update_server(str(run.id))

        assert (
            str(e_info.value)
            == 'could not translate host name "a" to address: nodename nor servname provided, or not known\n'
            or str(e_info.value)
            == 'could not translate host name "a" to address: Temporary failure in name resolution\n'
        )

    def test_run_update_server_no_connector(self, test_workspace, test_connector):
        connection = Connection.objects.create(
            name="C3", connector=test_connector, workspace=test_workspace
        )
        run = Run.objects.create(connection=connection, workspace=test_workspace)

        with pytest.raises(Exception) as e_info:
            run_update_server(str(run.id))

        assert str(e_info.value) == "No connector found for: Connector"


@pytest.mark.django_db
class TestConnectionSchedule:
    def test_run_connection_schedule_postgres(
        self, test_workspace, test_postgres_connector
    ):
        connection = Connection.objects.create(
            name="C4",
            connector=test_postgres_connector,
            workspace=test_workspace,
            metadata={"host": "a", "port": 5432, "dbname": "grai", "user": "grai"},
            secrets={"password": "grai"},
        )

        with pytest.raises(Exception) as e_info:
            run_connection_schedule(str(connection.id))

        assert (
            str(e_info.value)
            == 'could not translate host name "a" to address: nodename nor servname provided, or not known\n'
            or str(e_info.value)
            == 'could not translate host name "a" to address: Temporary failure in name resolution\n'
        )

    def test_run_connection_schedule_no_connector(self, test_workspace, test_connector):
        connection = Connection.objects.create(
            name="C5", connector=test_connector, workspace=test_workspace
        )

        with pytest.raises(Exception) as e_info:
            run_connection_schedule(str(connection.id))
        assert str(e_info.value) == "No connector found for: Connector"

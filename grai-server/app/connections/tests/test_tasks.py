import pytest
from django.test import TransactionTestCase
from decouple import config

from connections.models import Connection, Connector, Run
from connections.tasks import run_connection_schedule, run_update_server
from decouple import config
from django.test import TransactionTestCase
from workspaces.models import Workspace, Organisation


class TestUpdateServer(TransactionTestCase):
    @pytest.mark.django_db
    def test_run_update_server_postgres(self):
        organisation = Organisation.objects.create(name="Org1")
        workspace = Workspace.objects.create(name="W1", organisation=organisation)
        connector = Connector.objects.create(name="PostgreSQL")
        connection = Connection.objects.create(
            name="C1",
            connector=connector,
            workspace=workspace,
            metadata={
                "host": config("DB_HOST", "localhost"),
                "port": 5432,
                "dbname": "grai",
                "user": "grai",
            },
            secrets={"password": "grai"},
        )
        run = Run.objects.create(connection=connection, workspace=workspace)

        run_update_server(str(run.id))

    @pytest.mark.django_db
    def test_run_update_server_postgres_no_host(self):
        organisation = Organisation.objects.create(name="Org1")
        workspace = Workspace.objects.create(name="W1", organisation=organisation)
        connector = Connector.objects.create(name="PostgreSQL")
        connection = Connection.objects.create(
            name="C1",
            connector=connector,
            workspace=workspace,
            metadata={"host": "a", "port": 5432, "dbname": "grai", "user": "grai"},
            secrets={"password": "grai"},
        )
        run = Run.objects.create(connection=connection, workspace=workspace)

        with pytest.raises(Exception) as e_info:
            run_update_server(str(run.id))

        assert (
            str(e_info.value)
            == 'could not translate host name "a" to address: nodename nor servname provided, or not known\n'
            or str(e_info.value)
            == 'could not translate host name "a" to address: Temporary failure in name resolution\n'
        )

    @pytest.mark.django_db
    def test_run_update_server_no_connector(self):
        organisation = Organisation.objects.create(name="Org1")
        workspace = Workspace.objects.create(name="W1", organisation=organisation)
        connector = Connector.objects.create(name="Connector")
        connection = Connection.objects.create(
            name="C1", connector=connector, workspace=workspace
        )
        run = Run.objects.create(connection=connection, workspace=workspace)

        with pytest.raises(Exception) as e_info:
            run_update_server(str(run.id))

        assert str(e_info.value) == "No connector found for: Connector"


class TestConnectionSchedule(TransactionTestCase):
    @pytest.mark.django_db
    def test_run_connection_schedule_postgres(self):
        organisation = Organisation.objects.create(name="Org1")
        workspace = Workspace.objects.create(name="W1", organisation=organisation)
        connector = Connector.objects.create(name="PostgreSQL")
        connection = Connection.objects.create(
            name="C1",
            connector=connector,
            workspace=workspace,
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

    @pytest.mark.django_db
    def test_run_connection_schedule_no_connector(self):
        organisation = Organisation.objects.create(name="Org1")
        workspace = Workspace.objects.create(name="W1", organisation=organisation)
        connector = Connector.objects.create(name="Connector")
        connection = Connection.objects.create(
            name="C1", connector=connector, workspace=workspace
        )

        with pytest.raises(Exception) as e_info:
            run_connection_schedule(str(connection.id))
        assert str(e_info.value) == "No connector found for: Connector"

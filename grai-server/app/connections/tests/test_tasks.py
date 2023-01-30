import os
import pytest
from decouple import config

from lineage.models import Node
from connections.models import Connection, Connector, Run, RunFile
from connections.tasks import run_connection_schedule, run_update_server
from workspaces.models import Organisation, Workspace
from django.core.files.uploadedfile import UploadedFile

__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))


@pytest.fixture
def test_organisation():
    return Organisation.objects.create(name="Org1")


@pytest.fixture
def test_workspace(test_organisation):
    return Workspace.objects.create(name="W10", organisation=test_organisation)


@pytest.fixture
def test_postgres_connector():
    return Connector.objects.create(name=Connector.POSTGRESQL)


@pytest.fixture
def test_dbt_connector():
    connector, created = Connector.objects.get_or_create(name=Connector.DBT)

    return connector


@pytest.fixture
def test_yaml_file_connector():
    connector, created = Connector.objects.get_or_create(name=Connector.YAMLFILE)

    return connector


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

    def test_run_update_server_postgres_no_host(self, test_workspace, test_postgres_connector):
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
        connection = Connection.objects.create(name="C3", connector=test_connector, workspace=test_workspace)
        run = Run.objects.create(connection=connection, workspace=test_workspace)

        with pytest.raises(Exception) as e_info:
            run_update_server(str(run.id))

        assert str(e_info.value) == "No connector found for: Connector"

    def test_run_update_server_dbt(self, test_workspace, test_dbt_connector):
        with open(os.path.join(__location__, "manifest.json")) as reader:
            file = UploadedFile(reader, name="manifest.json")

            run = Run.objects.create(connector=test_dbt_connector, workspace=test_workspace)
            RunFile.objects.create(run=run, file=file)

            run_update_server(str(run.id))

    def test_run_update_server_yaml_file(self, test_workspace, test_yaml_file_connector):
        Node.objects.create(workspace=test_workspace, namespace="default", name="table1")

        with open(os.path.join(__location__, "test.yaml")) as reader:
            file = UploadedFile(reader, name="test.yaml")

            run = Run.objects.create(connector=test_yaml_file_connector, workspace=test_workspace)
            RunFile.objects.create(run=run, file=file)

            run_update_server(str(run.id))


@pytest.mark.django_db
class TestConnectionSchedule:
    def test_run_connection_schedule_postgres(self, test_workspace, test_postgres_connector):
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
        connection = Connection.objects.create(name="C5", connector=test_connector, workspace=test_workspace)

        with pytest.raises(Exception) as e_info:
            run_connection_schedule(str(connection.id))
        assert str(e_info.value) == "No connector found for: Connector"

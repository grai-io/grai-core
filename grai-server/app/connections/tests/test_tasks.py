import os
import uuid

import pytest
from decouple import config
from django.core.files.uploadedfile import UploadedFile

from connections.models import Connection, Connector, Run, RunFile
from connections.tasks import process_run, run_connection_schedule
from installations.models import Branch, Commit, PullRequest, Repository
from installations.tests.test_github import mocked_requests_post
from lineage.models import Node
from workspaces.models import Organisation, Workspace

__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))


@pytest.fixture
def test_organisation():
    return Organisation.objects.create(name="Org1")


@pytest.fixture
def test_workspace(test_organisation):
    return Workspace.objects.create(name="W10", organisation=test_organisation)


@pytest.fixture
def test_postgres_connector():
    return Connector.objects.create(name=Connector.POSTGRESQL, slug=Connector.POSTGRESQL)


@pytest.fixture
def test_snowflake_connector():
    return Connector.objects.create(name=Connector.SNOWFLAKE, slug=Connector.SNOWFLAKE)


@pytest.fixture
def test_mssql_connector():
    return Connector.objects.create(name=Connector.MSSQL, slug=Connector.MSSQL)


@pytest.fixture
def test_bigquery_connector():
    return Connector.objects.create(name=Connector.BIGQUERY, slug=Connector.BIGQUERY)


@pytest.fixture
def test_fivetran_connector():
    return Connector.objects.create(name=Connector.FIVETRAN, slug=Connector.FIVETRAN)


@pytest.fixture
def test_mysql_connector():
    return Connector.objects.create(name=Connector.MYSQL, slug=Connector.MYSQL)


@pytest.fixture
def test_dbt_connector():
    connector, created = Connector.objects.get_or_create(name=Connector.DBT, slug=Connector.DBT)

    return connector


@pytest.fixture
def test_yaml_file_connector():
    connector, created = Connector.objects.get_or_create(name=Connector.YAMLFILE, slug=Connector.YAMLFILE)

    return connector


@pytest.fixture
def test_connector():
    return Connector.objects.create(name="Connector", slug="Connector")


@pytest.fixture
def test_repository(test_workspace):
    return Repository.objects.create(
        workspace=test_workspace, owner="test_owner", repo="test_repo", type=Repository.GITHUB, installation_id=1234
    )


@pytest.fixture
def test_branch(test_workspace, test_repository):
    return Branch.objects.create(workspace=test_workspace, repository=test_repository, reference=str(uuid.uuid4()))


@pytest.fixture
def test_pull_request(test_workspace, test_repository, test_branch):
    return PullRequest.objects.create(
        workspace=test_workspace,
        repository=test_repository,
        branch=test_branch,
        reference=str(uuid.uuid4()),
        title=str(uuid.uuid4()),
    )


@pytest.fixture
def test_commit(test_workspace, test_repository, test_branch):
    return Commit.objects.create(
        workspace=test_workspace,
        repository=test_repository,
        branch=test_branch,
        reference=str(uuid.uuid4()),
        title=str(uuid.uuid4()),
    )


@pytest.fixture
def test_commit_with_pr(test_workspace, test_repository, test_branch, test_pull_request):
    return Commit.objects.create(
        workspace=test_workspace,
        repository=test_repository,
        branch=test_branch,
        pull_request=test_pull_request,
        reference=str(uuid.uuid4()),
        title=str(uuid.uuid4()),
    )


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

        process_run(str(run.id))

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
            process_run(str(run.id))

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
            process_run(str(run.id))

        assert str(e_info.value) == "No connector found for: Connector"

    def test_run_update_server_dbt(self, test_workspace, test_dbt_connector):
        with open(os.path.join(__location__, "manifest.json")) as reader:
            file = UploadedFile(reader, name="manifest.json")
            connection = Connection.objects.create(
                name=str(uuid.uuid4()), connector=test_dbt_connector, workspace=test_workspace
            )
            run = Run.objects.create(connection=connection, workspace=test_workspace)
            RunFile.objects.create(run=run, file=file)

            process_run(str(run.id))

    def test_run_update_server_fivetran(self, test_workspace, test_fivetran_connector, mocker):
        mocker.patch("grai_source_fivetran.loader.FivetranConnector")
        mock = mocker.patch("grai_source_fivetran.base.get_nodes_and_edges")
        mock.return_value = [[], []]

        connection = Connection.objects.create(
            name="C1",
            connector=test_fivetran_connector,
            workspace=test_workspace,
            metadata={"api_key": "abc123"},
            secrets={"api_secret": "abc123"},
        )

        run = Run.objects.create(connection=connection, workspace=test_workspace)

        process_run(str(run.id))

    def test_run_update_server_fivetran_extras(self, test_workspace, test_fivetran_connector, mocker):
        mocker.patch("grai_source_fivetran.loader.FivetranConnector")
        mock = mocker.patch("grai_source_fivetran.base.get_nodes_and_edges")
        mock.return_value = [[], []]

        connection = Connection.objects.create(
            name="C1",
            connector=test_fivetran_connector,
            workspace=test_workspace,
            metadata={
                "api_key": "abc123",
                "endpoint": "https://grai.io",
                "limit": "10",
            },
            secrets={"api_secret": "abc123"},
        )

        run = Run.objects.create(connection=connection, workspace=test_workspace)

        process_run(str(run.id))

    def test_run_update_server_mysql(self, test_workspace, test_mysql_connector, mocker):
        mocker.patch("grai_source_mysql.loader.MySQLConnector")
        mock = mocker.patch("grai_source_mysql.base.get_nodes_and_edges")
        mock.return_value = [[], []]

        connection = Connection.objects.create(
            name="C1",
            connector=test_mysql_connector,
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

        process_run(str(run.id))

    def test_run_update_server_yaml_file(self, test_workspace, test_yaml_file_connector):
        Node.objects.create(workspace=test_workspace, namespace="default", name="table1")

        with open(os.path.join(__location__, "test.yaml")) as reader:
            file = UploadedFile(reader, name="test.yaml")
            connection = Connection.objects.create(
                name=str(uuid.uuid4()), connector=test_yaml_file_connector, workspace=test_workspace
            )
            run = Run.objects.create(connection=connection, workspace=test_workspace)
            RunFile.objects.create(run=run, file=file)

            process_run(str(run.id))

    def test_snowflake_no_account(self, test_workspace, test_snowflake_connector, mocker):
        mock = mocker.patch("grai_source_snowflake.base.get_nodes_and_edges")
        mock.return_value = [[], []]

        connection = Connection.objects.create(
            name="C2",
            connector=test_snowflake_connector,
            workspace=test_workspace,
            metadata={
                "account": "account",
                "user": "user",
                "role": "role",
                "warehouse": "warehouse",
                "database": "database",
                "schema": "schema",
            },
            secrets={"password": "password1234"},
        )
        run = Run.objects.create(connection=connection, workspace=test_workspace)

        process_run(str(run.id))

    def test_mssql_no_account(self, test_workspace, test_mssql_connector, mocker):
        mock = mocker.patch("grai_source_mssql.base.get_nodes_and_edges")
        mock.return_value = [[], []]

        connection = Connection.objects.create(
            name="C2",
            connector=test_mssql_connector,
            workspace=test_workspace,
            metadata={
                "user": "user",
                "database": "database",
                "host": "a",
                "port": "1443",
            },
            secrets={"password": "password1234"},
        )
        run = Run.objects.create(connection=connection, workspace=test_workspace)

        process_run(str(run.id))

    def test_bigquery_no_project(self, test_workspace, test_bigquery_connector, mocker):
        mock = mocker.patch("grai_source_bigquery.base.get_nodes_and_edges")
        mock.return_value = [[], []]

        connection = Connection.objects.create(
            name="C2",
            connector=test_bigquery_connector,
            workspace=test_workspace,
            metadata={"project": "a", "dataset": "dataset"},
            secrets={"credentials": {}},
        )
        run = Run.objects.create(connection=connection, workspace=test_workspace)

        process_run(str(run.id))


@pytest.mark.django_db
class TestTests:
    def test_dbt(self, test_workspace, test_dbt_connector):
        with open(os.path.join(__location__, "manifest.json")) as reader:
            file = UploadedFile(reader, name="manifest.json")
            connection = Connection.objects.create(
                name=str(uuid.uuid4()), connector=test_dbt_connector, workspace=test_workspace
            )
            run = Run.objects.create(connection=connection, workspace=test_workspace, action=Run.TESTS)
            RunFile.objects.create(run=run, file=file)

        process_run(str(run.id))

    def test_dbt_github(self, test_workspace, test_dbt_connector, test_commit_with_pr, mocker):
        mocker.patch("installations.github.requests.post", side_effect=mocked_requests_post)
        mocker.patch("installations.github.GhApi")

        with open(os.path.join(__location__, "manifest.json")) as reader:
            file = UploadedFile(reader, name="manifest.json")
            connection = Connection.objects.create(
                name=str(uuid.uuid4()), connector=test_dbt_connector, workspace=test_workspace
            )
            run = Run.objects.create(
                connection=connection,
                workspace=test_workspace,
                commit=test_commit_with_pr,
                action=Run.TESTS,
                trigger={"check_id": "1234"},
            )
            RunFile.objects.create(run=run, file=file)

        process_run(str(run.id))

    def test_no_connector_github(self, test_workspace, test_connector, test_commit, mocker):
        mocker.patch("installations.github.requests.post", side_effect=mocked_requests_post)
        mocker.patch("installations.github.GhApi")

        connection = Connection.objects.create(name="C3", connector=test_connector, workspace=test_workspace)
        run = Run.objects.create(
            connection=connection,
            workspace=test_workspace,
            commit=test_commit,
            action=Run.TESTS,
            trigger={"check_id": "1234"},
        )

        with pytest.raises(Exception) as e_info:
            process_run(str(run.id))

        assert str(e_info.value) == "No connector found for: Connector"


@pytest.mark.django_db
class TestValidateTests:
    def test_validate_dbt(self, test_workspace, test_dbt_connector):
        with open(os.path.join(__location__, "manifest.json")) as reader:
            file = UploadedFile(reader, name="manifest.json")
            connection = Connection.objects.create(
                name=str(uuid.uuid4()), connector=test_dbt_connector, workspace=test_workspace
            )
            run = Run.objects.create(connection=connection, workspace=test_workspace, action=Run.VALIDATE)
            RunFile.objects.create(run=run, file=file)

        process_run(str(run.id))


@pytest.mark.django_db
def test_process_run_incorrect_action(test_workspace, test_yaml_file_connector):
    Node.objects.create(workspace=test_workspace, namespace="default", name="table1")

    with open(os.path.join(__location__, "test.yaml")) as reader:
        file = UploadedFile(reader, name="test.yaml")
        connection = Connection.objects.create(
            name=str(uuid.uuid4()), connector=test_yaml_file_connector, workspace=test_workspace
        )
        run = Run.objects.create(connection=connection, workspace=test_workspace, action="Incorrect")
        RunFile.objects.create(run=run, file=file)

        with pytest.raises(Exception) as e_info:
            process_run(str(run.id))

        assert str(e_info.value) == "Incorrect run action Incorrect found, accepted values: tests, update"


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

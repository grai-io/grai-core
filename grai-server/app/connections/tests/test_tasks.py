import os
import uuid
from datetime import date
from unittest import mock

import pytest
from decouple import config
from django.conf import settings
from django.core.files.uploadedfile import UploadedFile
from grai_source_dbt_cloud.loader import Event

from connections.models import Connection, Connector, Run, RunFile
from connections.tasks import process_run, run_connection_schedule
from installations.models import Branch, Commit, PullRequest, Repository
from installations.tests.test_github import mocked_requests_post
from lineage.models import Edge, Node, Source
from workspaces.models import Organisation, Workspace

__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))


@pytest.fixture
def test_organisation():
    return Organisation.objects.create(name=str(uuid.uuid4()))


@pytest.fixture
def test_workspace(test_organisation):
    return Workspace.objects.create(name=str(uuid.uuid4()), organisation=test_organisation)


@pytest.fixture
def test_source(test_workspace):
    return Source.objects.create(workspace=test_workspace, name=str(uuid.uuid4()))


@pytest.fixture
def test_postgres_connector():
    connector, created = Connector.objects.get_or_create(name=Connector.POSTGRESQL, slug=Connector.POSTGRESQL)

    return connector


@pytest.fixture
def test_snowflake_connector():
    connector, created = Connector.objects.get_or_create(name=Connector.SNOWFLAKE, slug=Connector.SNOWFLAKE)

    return connector


@pytest.fixture
def test_mssql_connector():
    connector, created = Connector.objects.get_or_create(name=Connector.MSSQL, slug=Connector.MSSQL)

    return connector


@pytest.fixture
def test_bigquery_connector():
    connector, created = Connector.objects.get_or_create(name=Connector.BIGQUERY, slug=Connector.BIGQUERY)

    return connector


@pytest.fixture
def test_dbt_cloud_connector():
    connector, created = Connector.objects.get_or_create(name=Connector.DBT_CLOUD, slug=Connector.DBT_CLOUD)

    return connector


@pytest.fixture
def test_fivetran_connector():
    connector, created = Connector.objects.get_or_create(name=Connector.FIVETRAN, slug=Connector.FIVETRAN)

    return connector


@pytest.fixture
def test_mysql_connector():
    connector, created = Connector.objects.get_or_create(name=Connector.MYSQL, slug=Connector.MYSQL)

    return connector


@pytest.fixture
def test_redshift_connector():
    connector, created = Connector.objects.get_or_create(name=Connector.REDSHIFT, slug=Connector.REDSHIFT)

    return connector


@pytest.fixture
def test_dbt_connector():
    connector, created = Connector.objects.get_or_create(name=Connector.DBT, slug=Connector.DBT)

    return connector


@pytest.fixture
def test_metabase_connector():
    connector, created = Connector.objects.get_or_create(name=Connector.METABASE, slug=Connector.METABASE)

    return connector


@pytest.fixture
def test_looker_connector():
    connector, created = Connector.objects.get_or_create(name=Connector.LOOKER, slug=Connector.LOOKER)

    return connector


@pytest.fixture
def test_yaml_file_connector():
    connector, created = Connector.objects.get_or_create(name=Connector.YAMLFILE, slug=Connector.YAMLFILE)

    return connector


@pytest.fixture
def test_connector():
    connector, created = Connector.objects.get_or_create(name="Connector", slug="Connector")

    return connector


@pytest.fixture
def test_repository(test_workspace):
    return Repository.objects.create(
        workspace=test_workspace,
        owner="test_owner",
        repo="test_repo",
        type=Repository.GITHUB,
        installation_id=1234,
    )


@pytest.fixture
def test_branch(test_workspace, test_repository):
    return Branch.objects.create(
        workspace=test_workspace,
        repository=test_repository,
        reference=str(uuid.uuid4()),
    )


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
    def test_run_update_server_postgres(self, test_workspace, test_postgres_connector, test_source):
        connection = Connection.objects.create(
            name=str(uuid.uuid4()),
            connector=test_postgres_connector,
            workspace=test_workspace,
            source=test_source,
            metadata={
                "host": config("DB_HOST", "localhost"),
                "port": 5432,
                "dbname": "grai",
                "user": "grai",
            },
            secrets={"password": "grai"},
        )
        run = Run.objects.create(connection=connection, workspace=test_workspace, source=test_source)

        process_run(str(run.id))

    def test_run_update_server_postgres_no_host(self, test_workspace, test_postgres_connector, test_source):
        connection = Connection.objects.create(
            name=str(uuid.uuid4()),
            connector=test_postgres_connector,
            workspace=test_workspace,
            source=test_source,
            metadata={"host": "a", "port": 5432, "dbname": "grai", "user": "grai"},
            secrets={"password": "grai"},
        )
        run = Run.objects.create(connection=connection, workspace=test_workspace, source=test_source)

        with pytest.raises(Exception) as e_info:
            process_run(str(run.id))

        assert (
            str(e_info.value)
            == 'could not translate host name "a" to address: nodename nor servname provided, or not known\n'
            or str(e_info.value)
            == 'could not translate host name "a" to address: Temporary failure in name resolution\n'
        )

    def test_run_update_server_no_connector(self, test_workspace, test_connector, test_source):
        connection = Connection.objects.create(
            name=str(uuid.uuid4()),
            connector=test_connector,
            workspace=test_workspace,
            source=test_source,
        )
        run = Run.objects.create(connection=connection, workspace=test_workspace, source=test_source)

        with pytest.raises(Exception) as e_info:
            process_run(str(run.id))

        assert str(e_info.value) == "No connector found for: Connector"

    def test_run_update_server_dbt(self, test_workspace, test_dbt_connector, test_source):
        with open(os.path.join(__location__, "manifest.json")) as reader:
            file = UploadedFile(reader, name="manifest.json")
            connection = Connection.objects.create(
                name=str(uuid.uuid4()),
                connector=test_dbt_connector,
                workspace=test_workspace,
                source=test_source,
            )
            run = Run.objects.create(connection=connection, workspace=test_workspace, source=test_source)
            RunFile.objects.create(run=run, file=file)

            process_run(str(run.id))

    @mock.patch("grai_source_fivetran.base.FivetranIntegration")
    def test_run_update_server_fivetran(self, mocked_class, test_workspace, test_fivetran_connector, test_source):
        mocked_class.return_value.get_nodes_and_edges.return_value = [[], []]

        connection = Connection.objects.create(
            name=str(uuid.uuid4()),
            connector=test_fivetran_connector,
            workspace=test_workspace,
            source=test_source,
            metadata={"api_key": "abc123"},
            secrets={"api_secret": "abc123"},
        )

        run = Run.objects.create(connection=connection, workspace=test_workspace, source=test_source)

        process_run(str(run.id))

    @mock.patch("grai_source_fivetran.base.FivetranIntegration")
    def test_run_update_server_fivetran_extras(
        self, mocked_class, test_workspace, test_fivetran_connector, test_source
    ):
        mocked_class.return_value.get_nodes_and_edges.return_value = [[], []]

        connection = Connection.objects.create(
            name=str(uuid.uuid4()),
            connector=test_fivetran_connector,
            workspace=test_workspace,
            source=test_source,
            metadata={
                "api_key": "abc123",
                "endpoint": "https://grai.io",
                "limit": "10",
            },
            secrets={"api_secret": "abc123"},
        )

        run = Run.objects.create(connection=connection, workspace=test_workspace, source=test_source)

        process_run(str(run.id))

    @mock.patch("grai_source_mysql.base.MySQLIntegration")
    def test_run_update_server_mysql(self, mocked_class, test_workspace, test_mysql_connector, test_source):
        mocked_class.return_value.get_nodes_and_edges.return_value = [[], []]

        connection = Connection.objects.create(
            name=str(uuid.uuid4()),
            connector=test_mysql_connector,
            workspace=test_workspace,
            source=test_source,
            metadata={
                "host": config("DB_HOST", "localhost"),
                "port": 5432,
                "dbname": "grai",
                "user": "grai",
            },
            secrets={"password": "grai"},
        )

        run = Run.objects.create(connection=connection, workspace=test_workspace, source=test_source)

        process_run(str(run.id))

    @mock.patch("grai_source_redshift.base.RedshiftIntegration")
    def test_run_update_server_redshift(self, mocked_class, test_workspace, test_redshift_connector, test_source):
        mocked_class.return_value.get_nodes_and_edges.return_value = [[], []]

        connection = Connection.objects.create(
            name=str(uuid.uuid4()),
            connector=test_redshift_connector,
            workspace=test_workspace,
            source=test_source,
            metadata={
                "host": config("DB_HOST", "localhost"),
                "port": 5432,
                "database": "grai",
                "user": "grai",
            },
            secrets={"password": "grai"},
        )

        run = Run.objects.create(connection=connection, workspace=test_workspace, source=test_source)

        process_run(str(run.id))

    def test_run_update_server_yaml_file(self, test_workspace, test_yaml_file_connector, test_source):
        Node.objects.create(workspace=test_workspace, namespace="default", name="table1")

        with open(os.path.join(__location__, "test.yaml")) as reader:
            file = UploadedFile(reader, name="test.yaml")
            connection = Connection.objects.create(
                name=str(uuid.uuid4()),
                connector=test_yaml_file_connector,
                workspace=test_workspace,
                source=test_source,
            )
            run = Run.objects.create(connection=connection, workspace=test_workspace, source=test_source)
            RunFile.objects.create(run=run, file=file)

            process_run(str(run.id))

    @mock.patch("grai_source_snowflake.base.SnowflakeIntegration")
    def test_snowflake_no_account(self, mocked_class, test_workspace, test_snowflake_connector, test_source):
        mocked_class.return_value.get_nodes_and_edges.return_value = [[], []]

        connection = Connection.objects.create(
            name=str(uuid.uuid4()),
            connector=test_snowflake_connector,
            workspace=test_workspace,
            source=test_source,
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
        run = Run.objects.create(connection=connection, workspace=test_workspace, source=test_source)

        process_run(str(run.id))

    @mock.patch("grai_source_mssql.base.MsSQLIntegration")
    def test_mssql_no_account(self, mocked_class, test_workspace, test_mssql_connector, test_source):
        mocked_class.return_value.get_nodes_and_edges.return_value = [[], []]

        connection = Connection.objects.create(
            name=str(uuid.uuid4()),
            connector=test_mssql_connector,
            workspace=test_workspace,
            source=test_source,
            metadata={
                "user": "user",
                "database": "database",
                "host": "a",
                "port": "1443",
                "driver": "test",
            },
            secrets={"password": "password1234"},
        )
        run = Run.objects.create(connection=connection, workspace=test_workspace, source=test_source)

        process_run(str(run.id))

    @mock.patch("grai_source_bigquery.base.BigQueryIntegration")
    def test_bigquery_no_project(self, mocked_class, test_workspace, test_bigquery_connector, test_source):
        mocked_class.return_value.get_nodes_and_edges.return_value = [[], []]

        connection = Connection.objects.create(
            name=str(uuid.uuid4()),
            connector=test_bigquery_connector,
            workspace=test_workspace,
            source=test_source,
            metadata={"project": "a", "dataset": "dataset"},
            secrets={"credentials": {}},
        )
        run = Run.objects.create(connection=connection, workspace=test_workspace, source=test_source)

        process_run(str(run.id))

    @mock.patch("grai_source_metabase.base.MetabaseIntegration")
    def test_metabase_no_account(self, mocked_class, test_workspace, test_metabase_connector, test_source):
        mocked_class.return_value.get_nodes_and_edges.return_value = [[], []]

        connection = Connection.objects.create(
            name=str(uuid.uuid4()),
            connector=test_metabase_connector,
            workspace=test_workspace,
            source=test_source,
            metadata={
                "endpoint": "https://metabase-test.com",
                "username": "user",
            },
            secrets={"password": "password1234"},
        )
        run = Run.objects.create(connection=connection, workspace=test_workspace, source=test_source)

        process_run(str(run.id))

    @mock.patch("grai_source_looker.base.LookerIntegration")
    def test_looker_no_account(self, mocked_class, test_workspace, test_looker_connector, test_source):
        mocked_class.return_value.get_nodes_and_edges.return_value = [[], []]

        connection = Connection.objects.create(
            name=str(uuid.uuid4()),
            connector=test_looker_connector,
            workspace=test_workspace,
            source=test_source,
            metadata={
                "base_url": "https://looker-test.com",
                "client_id": "client_id",
            },
            secrets={"client_secret": "password1234"},
        )
        run = Run.objects.create(connection=connection, workspace=test_workspace, source=test_source)

        process_run(str(run.id))

    @mock.patch("grai_source_dbt_cloud.base.DbtCloudIntegration")
    def test_dbt_cloud_no_project(self, mocked_class, test_workspace, test_dbt_cloud_connector, test_source):
        mocked_class.return_value.get_nodes_and_edges.return_value = [[], []]

        connection = Connection.objects.create(
            name=str(uuid.uuid4()),
            connector=test_dbt_cloud_connector,
            workspace=test_workspace,
            source=test_source,
            metadata={},
            secrets={"api_key": "abc1234"},
        )
        run = Run.objects.create(connection=connection, workspace=test_workspace, source=test_source)

        process_run(str(run.id))


@pytest.mark.django_db
class TestTests:
    def test_dbt(self, test_workspace, test_dbt_connector, test_source):
        with open(os.path.join(__location__, "manifest.json")) as reader:
            file = UploadedFile(reader, name="manifest.json")
            connection = Connection.objects.create(
                name=str(uuid.uuid4()),
                connector=test_dbt_connector,
                workspace=test_workspace,
                source=test_source,
            )
            run = Run.objects.create(
                connection=connection,
                workspace=test_workspace,
                action=Run.TESTS,
                source=test_source,
            )
            RunFile.objects.create(run=run, file=file)

        process_run(str(run.id))

    @pytest.mark.skipif(settings.GITHUB_PRIVATE_KEY is None, reason="requires github credentials")
    def test_dbt_github(
        self,
        test_workspace,
        test_dbt_connector,
        test_commit_with_pr,
        mocker,
        test_source,
    ):
        mocker.patch("installations.github.requests.post", side_effect=mocked_requests_post)
        mocker.patch("installations.github.GhApi")

        with open(os.path.join(__location__, "manifest.json")) as reader:
            file = UploadedFile(reader, name="manifest.json")
            connection = Connection.objects.create(
                name=str(uuid.uuid4()),
                connector=test_dbt_connector,
                workspace=test_workspace,
                source=test_source,
            )
            run = Run.objects.create(
                connection=connection,
                workspace=test_workspace,
                commit=test_commit_with_pr,
                action=Run.TESTS,
                trigger={"check_id": "1234"},
                source=test_source,
            )
            RunFile.objects.create(run=run, file=file)

        process_run(str(run.id))

    @pytest.mark.skipif(settings.GITHUB_PRIVATE_KEY is None, reason="requires github credentials")
    def test_no_connector_github(self, test_workspace, test_connector, test_commit, mocker, test_source):
        mocker.patch("installations.github.requests.post", side_effect=mocked_requests_post)
        mocker.patch("installations.github.GhApi")

        connection = Connection.objects.create(
            name=str(uuid.uuid4()),
            connector=test_connector,
            workspace=test_workspace,
            source=test_source,
        )
        run = Run.objects.create(
            connection=connection,
            workspace=test_workspace,
            commit=test_commit,
            action=Run.TESTS,
            trigger={"check_id": "1234"},
            source=test_source,
        )

        with pytest.raises(Exception) as e_info:
            process_run(str(run.id))

        assert str(e_info.value) == "No connector found for: Connector"

    @pytest.mark.skipif(settings.GITHUB_PRIVATE_KEY is None, reason="requires github credentials")
    def test_dbt_github_test_failure(
        self,
        test_workspace,
        test_dbt_connector,
        test_commit_with_pr,
        mocker,
        test_source,
    ):
        mocker.patch("installations.github.requests.post", side_effect=mocked_requests_post)
        mocker.patch("installations.github.GhApi")

        source = Node.objects.create(
            workspace=test_workspace,
            namespace="default",
            name="public.customers.customer_id",
            display_name="customer_id",
            is_active=True,
            metadata={
                "grai": {
                    "version": "v1",
                    "node_type": "Column",
                    "node_attibutes": {
                        "data_type": "string",
                        "is_nullable": True,
                        "is_unique": False,
                    },
                }
            },
        )

        destination = Node.objects.create(
            workspace=test_workspace,
            namespace="default",
            name="column2",
            display_name="column2",
            is_active=True,
            metadata={
                "grai": {
                    "version": "v1",
                    "node_type": "Column",
                    "node_attributes": {
                        "data_type": "string",
                        "default_value": None,
                        "is_nullable": True,
                        "is_unique": True,
                        "is_primary_key": False,
                    },
                }
            },
        )

        Edge.objects.create(
            workspace=test_workspace,
            source=source,
            destination=destination,
            is_active=True,
            name="column1_column2",
            namespace="default",
            metadata={
                "grai": {
                    "version": "v1",
                    "edge_type": "ColumnToColumn",
                    "edge_attributes": {
                        "preserves_data_type": True,
                        "preserves_nullable": True,
                        "preserves_unique": True,
                    },
                }
            },
        )

        with open(os.path.join(__location__, "manifest.json")) as reader:
            file = UploadedFile(reader, name="manifest.json")
            connection = Connection.objects.create(
                name=str(uuid.uuid4()),
                connector=test_dbt_connector,
                workspace=test_workspace,
                source=test_source,
            )
            run = Run.objects.create(
                connection=connection,
                workspace=test_workspace,
                commit=test_commit_with_pr,
                action=Run.TESTS,
                trigger={"check_id": "1234"},
                source=test_source,
            )
            RunFile.objects.create(run=run, file=file)

        process_run(str(run.id))

    @pytest.mark.skipif(settings.GITHUB_PRIVATE_KEY is None, reason="requires github credentials")
    def test_yaml_github_test_failure(
        self,
        test_workspace,
        test_yaml_file_connector,
        test_commit_with_pr,
        mocker,
        test_source,
    ):
        mocker.patch("installations.github.requests.post", side_effect=mocked_requests_post)
        mocker.patch("installations.github.GhApi")

        source = Node.objects.create(
            workspace=test_workspace,
            namespace="default",
            name="column1",
            display_name="column1",
            is_active=True,
            metadata={
                "grai": {
                    "version": "v1",
                    "node_type": "Column",
                    "node_attibutes": {
                        "data_type": "string",
                        "is_nullable": True,
                        "is_unique": False,
                    },
                }
            },
        )

        destination = Node.objects.create(
            workspace=test_workspace,
            namespace="default",
            name="column2",
            display_name="column2",
            is_active=True,
            metadata={
                "grai": {
                    "version": "v1",
                    "node_type": "Column",
                    "node_attibutes": {
                        "data_type": "string",
                        "default_value": None,
                        "is_nullable": False,
                        "is_unique": True,
                        "is_primary_key": False,
                    },
                }
            },
        )

        Edge.objects.create(
            workspace=test_workspace,
            source=source,
            destination=destination,
            is_active=True,
            name="column1_column2",
            namespace="default",
            metadata={
                "grai": {
                    "version": "v1",
                    "edge_type": "ColumnToColumn",
                    "edge_attributes": {
                        "preserves_data_type": True,
                        "preserves_nullable": True,
                        "preserves_unique": True,
                    },
                }
            },
        )

        with open(os.path.join(__location__, "test.yaml")) as reader:
            file = UploadedFile(reader, name="test.yaml")
            connection = Connection.objects.create(
                name=str(uuid.uuid4()),
                connector=test_yaml_file_connector,
                workspace=test_workspace,
                source=test_source,
            )
            run = Run.objects.create(
                connection=connection,
                workspace=test_workspace,
                commit=test_commit_with_pr,
                action=Run.TESTS,
                trigger={"check_id": "1234"},
                source=test_source,
            )
            RunFile.objects.create(run=run, file=file)

        process_run(str(run.id))


@pytest.mark.django_db
class TestValidateTests:
    def test_validate_dbt(self, test_workspace, test_dbt_connector, test_source):
        with open(os.path.join(__location__, "manifest.json")) as reader:
            file = UploadedFile(reader, name="manifest.json")
            connection = Connection.objects.create(
                name=str(uuid.uuid4()),
                connector=test_dbt_connector,
                workspace=test_workspace,
                source=test_source,
            )
            run = Run.objects.create(
                connection=connection,
                workspace=test_workspace,
                action=Run.VALIDATE,
                source=test_source,
            )
            RunFile.objects.create(run=run, file=file)

        process_run(str(run.id))


@pytest.mark.django_db
def test_process_run_incorrect_action(test_workspace, test_yaml_file_connector, test_source):
    Node.objects.create(workspace=test_workspace, namespace="default", name="table1")

    with open(os.path.join(__location__, "test.yaml")) as reader:
        file = UploadedFile(reader, name="test.yaml")
        connection = Connection.objects.create(
            name=str(uuid.uuid4()),
            connector=test_yaml_file_connector,
            workspace=test_workspace,
            source=test_source,
        )
        run = Run.objects.create(
            connection=connection,
            workspace=test_workspace,
            action="Incorrect",
            source=test_source,
        )
        RunFile.objects.create(run=run, file=file)

        with pytest.raises(Exception) as e_info:
            process_run(str(run.id))

        assert (
            str(e_info.value)
            == "Incorrect run action Incorrect found, accepted values: tests, update, validate, events, events_all"
        )


@pytest.mark.django_db
class TestConnectionSchedule:
    def test_run_connection_schedule_postgres(self, test_workspace, test_postgres_connector, test_source):
        connection = Connection.objects.create(
            name=str(uuid.uuid4()),
            connector=test_postgres_connector,
            workspace=test_workspace,
            metadata={"host": "a", "port": 5432, "dbname": "grai", "user": "grai"},
            secrets={"password": "grai"},
            source=test_source,
        )

        with pytest.raises(Exception) as e_info:
            run_connection_schedule(str(connection.id))

        assert (
            str(e_info.value)
            == 'could not translate host name "a" to address: nodename nor servname provided, or not known\n'
            or str(e_info.value)
            == 'could not translate host name "a" to address: Temporary failure in name resolution\n'
        )

    def test_run_connection_schedule_no_connector(self, test_workspace, test_connector, test_source):
        connection = Connection.objects.create(
            name=str(uuid.uuid4()),
            connector=test_connector,
            workspace=test_workspace,
            source=test_source,
        )

        with pytest.raises(Exception) as e_info:
            run_connection_schedule(str(connection.id))
        assert str(e_info.value) == "No connector found for: Connector"


@pytest.mark.django_db
class TestEventsTests:
    def test_dbt_cloud(self, test_workspace, test_dbt_cloud_connector, mocker, test_source):
        mock = mocker.patch("grai_source_dbt_cloud.base.DbtCloudIntegration.events")
        mock.return_value = [
            Event(
                reference="1234",
                date=date.today(),
                metadata={},
                status="success",
                nodes=[],
            )
        ]

        connection = Connection.objects.create(
            name=str(uuid.uuid4()),
            connector=test_dbt_cloud_connector,
            workspace=test_workspace,
            metadata={},
            secrets={"api_key": "abc1234"},
            source=test_source,
        )
        run = Run.objects.create(
            connection=connection,
            workspace=test_workspace,
            action=Run.EVENTS,
            source=test_source,
        )

        process_run(str(run.id))


@pytest.mark.django_db
class TestEventsAllTests:
    def test_dbt_cloud(self, test_workspace, test_dbt_cloud_connector, mocker):
        node = Node.objects.create(workspace=test_workspace, name=str(uuid.uuid4()))

        mock = mocker.patch("grai_source_dbt_cloud.base.DbtCloudIntegration.events")
        mock.return_value = [
            Event(
                reference="1234",
                date=date.today(),
                metadata={},
                status="success",
                nodes=[str(node.id)],
            )
        ]

        connection = Connection.objects.create(
            name=str(uuid.uuid4()),
            connector=test_dbt_cloud_connector,
            workspace=test_workspace,
            metadata={},
            secrets={"api_key": "abc1234"},
            source=test_source,
        )
        run = Run.objects.create(
            connection=connection,
            workspace=test_workspace,
            action=Run.EVENTS,
            source=test_source,
        )

        process_run(str(run.id))


@pytest.mark.django_db
class TestEventsAllTests:
    def test_dbt_cloud(self, test_workspace, test_dbt_cloud_connector, mocker, test_source):
        node = Node.objects.create(workspace=test_workspace, name=str(uuid.uuid4()))

        mock = mocker.patch("grai_source_dbt_cloud.base.DbtCloudIntegration.events")
        mock.return_value = [
            Event(
                reference="1234",
                date=date.today(),
                metadata={},
                status="success",
                nodes=[str(node.id)],
            )
        ]

        connection = Connection.objects.create(
            name=str(uuid.uuid4()),
            connector=test_dbt_cloud_connector,
            workspace=test_workspace,
            metadata={},
            secrets={"api_key": "abc1234"},
            source=test_source,
        )
        run = Run.objects.create(
            connection=connection,
            workspace=test_workspace,
            action=Run.EVENTS_ALL,
            source=test_source,
        )

        process_run(str(run.id))

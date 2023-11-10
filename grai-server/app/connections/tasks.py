import traceback
from enum import Enum
from typing import Type

from django.utils import timezone

from celery import shared_task
from grai_schemas.integrations.errors import NoConnectionError, IncorrectPasswordError, MissingPermissionError
from connections.adapters.base import BaseAdapter
from connections.adapters.bigquery import BigqueryAdapter
from connections.adapters.dbt import DbtAdapter
from connections.adapters.dbt_cloud import DbtCloudAdapter
from connections.adapters.fivetran import FivetranAdapter
from connections.adapters.looker import LookerAdapter
from connections.adapters.metabase import MetabaseAdapter
from connections.adapters.mssql import MssqlAdapter
from connections.adapters.mysql import MySQLAdapter
from connections.adapters.open_lineage import OpenLineageAdapter
from connections.adapters.postgres import PostgresAdapter
from connections.adapters.redshift import RedshiftAdapter
from connections.adapters.snowflake import SnowflakeAdapter
from connections.adapters.yaml_file import YamlFileAdapter
from installations.github import Github
from notifications.notifications import send_notification

from .models import Connection, Connector, Run


@shared_task
def process_run(runId):
    print(f"Task starting {runId}")
    run = Run.objects.get(pk=runId)
    execute_run(run)


@shared_task
def run_connection_schedule(connectionId):
    connection = Connection.objects.get(pk=connectionId)
    run = Run.objects.create(
        workspace=connection.workspace,
        connection=connection,
        status="queued",
        source=connection.source,
    )
    execute_run(run)


def get_adapter(slug: str) -> Type[BaseAdapter]:
    if slug == Connector.POSTGRESQL:
        return PostgresAdapter
    elif slug == Connector.SNOWFLAKE:
        return SnowflakeAdapter
    elif slug == Connector.DBT:
        return DbtAdapter
    elif slug == Connector.DBT_CLOUD:
        return DbtCloudAdapter
    elif slug == Connector.YAMLFILE:
        return YamlFileAdapter
    elif slug == Connector.MSSQL:
        return MssqlAdapter
    elif slug == Connector.BIGQUERY:
        return BigqueryAdapter
    elif slug == Connector.FIVETRAN:
        return FivetranAdapter
    elif slug == Connector.MYSQL:
        return MySQLAdapter
    elif slug == Connector.REDSHIFT:
        return RedshiftAdapter
    elif slug == Connector.METABASE:
        return MetabaseAdapter
    elif slug == Connector.LOOKER:
        return LookerAdapter
    elif slug == Connector.OPEN_LINEAGE:
        return OpenLineageAdapter

    raise NoConnectorError(f"No connector found for: {slug}")


def get_github_api(run: Run):
    repository = run.commit.repository

    return Github(
        owner=repository.owner,
        repo=repository.repo,
        installation_id=repository.installation_id,
    )


class GitHubMessages(Enum):
    UPDATE = "Update ran successfully"
    VALIDATE = "Validate ran successfully"
    EVENTS = "Events ran successfully"
    EVENTS_ALL = "All Events ran successfully"


def execute_run(run: Run):
    # Set run status to running
    run.status = "running"
    run.started_at = timezone.now()
    run.save()

    try:
        if run.commit and run.trigger:
            github = get_github_api(run)
            github.start_check(check_id=run.trigger["check_id"])

        has_failures = False

        connector = run.connection.connector
        adapter = get_adapter(connector.slug)(run)

        if run.action == Run.UPDATE:
            adapter.run_update()
            message = GitHubMessages.UPDATE.value
        elif run.action == Run.TESTS:
            results, message = adapter.run_tests()
            run.metadata = {"results": results}
            has_failures = len(list(result for result in results if not result["test_pass"])) > 0

            if has_failures:
                send_notification.delay("test_failure", "Test failures")
        elif run.action == Run.VALIDATE:
            adapter.run_validate()
            message = GitHubMessages.VALIDATE.value
            connection = run.connection
            connection.validated = True
            connection.save()
        elif run.action == Run.EVENTS:
            adapter.run_events()
            message = GitHubMessages.EVENTS.value
        elif run.action == Run.EVENTS_ALL:
            adapter.run_events(run_all=True)
            message = GitHubMessages.EVENTS_ALL.value
        else:
            raise NoActionError(
                f"Incorrect run action {run.action} found, accepted values: tests, update, validate, events, events_all"
            )

        run.status = "success"
        run.finished_at = timezone.now()
        run.save()

        if run.commit and run.trigger:
            github = get_github_api(run)
            github.complete_check(
                check_id=run.trigger["check_id"],
                conclusion="failure" if has_failures else "success",
            )
            if run.commit.pull_request:
                github.post_comment(run.commit.pull_request.reference, message)

    except NoConnectionError:
        error_run(run, {"error": "No connection"})

    except IncorrectPasswordError:
        error_run(run, {"error": "Incorrect password"})

    except MissingPermissionError:
        error_run(run, {"error": "Missing permission"})

    except Exception as e:
        error_run(run, {"error": str(e), "traceback": traceback.format_exc()})

        raise e


def error_run(run: Run, metadata: dict):
    run.metadata = metadata
    run.status = "error"
    run.finished_at = timezone.now()
    run.save()

    if run.commit and run.trigger:
        github = get_github_api(run)
        github.complete_check(check_id=run.trigger["check_id"], conclusion="failure")


class NoConnectorError(Exception):
    """raise this when no connection is found"""


class NoActionError(Exception):
    """raise this when no action is found"""

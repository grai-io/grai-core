from datetime import datetime

from celery import shared_task
from connections.adapters.base import BaseAdapter
from connections.adapters.bigquery import BigqueryAdapter
from connections.adapters.dbt import DbtAdapter
from connections.adapters.fivetran import FivetranAdapter
from connections.adapters.mssql import MssqlAdapter
from connections.adapters.mysql import MySQLAdapter
from connections.adapters.postgres import PostgresAdapter
from connections.adapters.snowflake import SnowflakeAdapter
from connections.adapters.yaml_file import YamlFileAdapter
from installations.github import Github

from .models import Connection, Connector, Run


@shared_task
def process_run(runId):
    print(f"Task starting {runId}")
    run = Run.objects.get(pk=runId)
    execute_run(run)


@shared_task
def run_connection_schedule(connectionId):
    connection = Connection.objects.get(pk=connectionId)
    run = Run.objects.create(workspace=connection.workspace, connection=connection, status="queued")
    execute_run(run)


def get_adapter(slug: str) -> BaseAdapter:
    if slug == Connector.POSTGRESQL:
        return PostgresAdapter()
    elif slug == Connector.SNOWFLAKE:
        return SnowflakeAdapter()
    elif slug == Connector.DBT:
        return DbtAdapter()
    elif slug == Connector.YAMLFILE:
        return YamlFileAdapter()
    elif slug == Connector.MSSQL:
        return MssqlAdapter()
    elif slug == Connector.BIGQUERY:
        return BigqueryAdapter()
    elif slug == Connector.FIVETRAN:
        return FivetranAdapter()
    elif slug == Connector.MYSQL:
        return MySQLAdapter()

    raise NoConnectorError(f"No connector found for: {slug}")


def get_github_api(run: Run):
    repository = run.commit.repository

    return Github(owner=repository.owner, repo=repository.repo, installation_id=repository.installation_id)


def execute_run(run: Run):
    # Set run status to running
    run.status = "running"
    run.started_at = datetime.now()
    run.save()

    if run.commit and run.trigger:
        github = get_github_api(run)
        github.start_check(check_id=run.trigger["check_id"])

    try:
        results = None

        connector = run.connection.connector
        adapter = get_adapter(connector.slug)

        if run.action == Run.UPDATE:
            adapter.run_update(run)
        elif run.action == Run.TESTS:
            results, message = adapter.run_tests(run)
            run.metadata = {"results": results}
        elif run.action == Run.VALIDATE:
            adapter.run_validate(run)
        else:
            raise NoActionError(f"Incorrect run action {run.action} found, accepted values: tests, update")

        run.status = "success"
        run.finished_at = datetime.now()
        run.save()

        if run.commit and run.trigger:
            github = get_github_api(run)
            github.complete_check(
                check_id=run.trigger["check_id"],
                conclusion="success" if results is None else "failure",
            )
            if run.commit.pull_request:
                github.post_comment(run.commit.pull_request.reference, message)
    except Exception as e:
        run.metadata = {"error": str(e)}
        run.status = "error"
        run.finished_at = datetime.now()
        run.save()

        if run.commit and run.trigger:
            github = get_github_api(run)
            github.complete_check(check_id=run.trigger["check_id"], conclusion="failure")

        raise e


class NoConnectorError(Exception):
    """raise this when no connection is found"""


class NoActionError(Exception):
    """raise this when no action is found"""

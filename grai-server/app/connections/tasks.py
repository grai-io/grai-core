from datetime import datetime

from celery import shared_task
from connections.adapters.base import BaseAdapter
from connections.adapters.bigquery import BigqueryAdapter
from connections.adapters.dbt import DbtAdapter
from connections.adapters.mssql import MssqlAdapter
from connections.adapters.postgres import PostgresAdapter
from connections.adapters.snowflake import SnowflakeAdapter
from connections.adapters.yaml_file import YamlFileAdapter

from .github import Github
from .models import Connection, Connector, Run
from .task_helpers import get_node, update


@shared_task
def run_update_server(runId):
    print(f"Task starting {runId}")
    run = Run.objects.get(pk=runId)
    execute_run(run)


@shared_task
def run_connection_schedule(connectionId):
    connection = Connection.objects.get(pk=connectionId)
    run = Run.objects.create(workspace=connection.workspace, connection=connection, status="queued")
    execute_run(run)


def get_adapter(name: str) -> BaseAdapter:
    if name == Connector.POSTGRESQL:
        return PostgresAdapter()
    elif name == Connector.SNOWFLAKE:
        return SnowflakeAdapter()
    elif name == Connector.DBT:
        return DbtAdapter()
    elif name == Connector.YAMLFILE:
        return YamlFileAdapter()
    elif name == Connector.MSSQL:
        return MssqlAdapter()
    elif name == Connector.BIGQUERY:
        return BigqueryAdapter()

    raise NoConnectorError(f"No connector found for: {name}")


def execute_run(run: Run):
    # Set run status to running
    run.status = "running"
    run.started_at = datetime.now()
    run.save()

    if run.trigger:
        github = Github(
            owner=run.trigger["owner"], repo=run.trigger["repo"], installation_id=run.trigger["installation_id"]
        )
        github.start_check(check_id=run.trigger["check_id"])

    try:
        connector = run.connection.connector
        adapter = get_adapter(connector.name)

        # update_server
        adapter.run_update(run)

        run.status = "success"
        run.finished_at = datetime.now()
        run.save()

        if run.trigger:
            github = Github(
                owner=run.trigger["owner"], repo=run.trigger["repo"], installation_id=run.trigger["installation_id"]
            )
            github.complete_check(check_id=run.trigger["check_id"])
    except Exception as e:
        run.metadata = {"error": str(e)}
        run.status = "error"
        run.finished_at = datetime.now()
        run.save()

        if run.trigger:
            github = Github(
                owner=run.trigger["owner"], repo=run.trigger["repo"], installation_id=run.trigger["installation_id"]
            )
            github.complete_check(check_id=run.trigger["check_id"], conclusion="failure")

        raise e


class NoConnectorError(Exception):
    """raise this when no connection is found"""

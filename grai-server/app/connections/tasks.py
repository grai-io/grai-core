from datetime import datetime

from celery import shared_task

from .models import Connection, Run
from .task_helpers import update


@shared_task
def run_update_server(runId):
    print(f"Task starting {runId}")
    run = Run.objects.get(pk=runId)
    execute_run(run)


@shared_task
def run_connection_schedule(connectionId):
    connection = Connection.objects.get(pk=connectionId)
    run = Run.objects.create(
        workspace=connection.workspace, connection=connection, status="queued"
    )
    execute_run(run)


def execute_run(run: Run):
    # Set run status to running
    run.status = "running"
    run.started_at = datetime.now()
    run.save()

    try:
        # update_server
        connector = run.connection.connector

        if connector.name == "PostgreSQL":
            run_postgres(run)
        else:
            raise NoConnectorError(f"No connector found for: {connector.name}")

        run.status = "success"
        run.finished_at = datetime.now()
        run.save()
    except Exception as e:
        run.metadata = {"error": str(e)}
        run.status = "error"
        run.finished_at = datetime.now()
        run.save()

        raise e


def run_postgres(run: Run):
    from grai_source_postgres.base import get_nodes_and_edges
    from grai_source_postgres.loader import PostgresConnector

    metadata = run.connection.metadata
    secrets = run.connection.secrets

    conn = PostgresConnector(
        host=metadata["host"],
        port=metadata["port"],
        dbname=metadata["dbname"],
        user=metadata["user"],
        password=secrets["password"],
    )
    nodes, edges = get_nodes_and_edges(conn, "v1")
    update(run.workspace, nodes)
    update(run.workspace, edges)


class NoConnectorError(Exception):
    """raise this when no connection is found"""

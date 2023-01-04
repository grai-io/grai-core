from typing import Dict, List, Optional, TypeVar

from .models import Run
from celery import shared_task
from datetime import datetime
from grai_client.schemas.edge import Edge, EdgeV1
from grai_client.schemas.node import Node, NodeV1, NodeID

from .task_helpers import update


@shared_task
def run_update_server(runId):
    print(f"Task starting {runId}")

    # Find run
    run = Run.objects.get(pk=runId)

    # Set run status to running
    run.status = "running"
    run.started_at = datetime.now()
    run.save()

    try:
        # update_server
        connector = run.connection.connector

        if connector.name == "Postgres":
            run_postgres(run)
        else:
            raise NoConnectorError("No connector found")

        run.status = "success"
        run.finished_at = datetime.now()
        run.save()
    except Exception as e:
        run.metadata = str(e)
        run.status = "error"
        run.finished_at = datetime.now()
        run.save()

        raise e


def run_postgres(run):
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

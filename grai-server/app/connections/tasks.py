from .models import Run
from celery import shared_task
from datetime import datetime


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


def run_postgres(run):
    from grai_client.endpoints.v1.client import ClientV1

    # TODO: update this to point to self
    client = ClientV1("localhost", "8000", workspace=run.workspace.id)
    # TODO: update this to use current user
    client.set_authentication_headers(username="null@grai.io", password="super_secret")
    # client.set_authentication_headers(api_key='qBzzVcCT.sVPZ3yVrv4e7oA9yzEtdrc1HwAOmLlsa')

    from grai_source_postgres.base import update_server

    metadata = run.connection.metadata
    secrets = run.connection.secrets

    update_server(
        client,
        host=metadata["host"],
        port=metadata["port"],
        dbname=metadata["dbname"],
        user=metadata["user"],
        password=secrets["password"],
        namespace=run.connection.namespace,
    )


class NoConnectorError(Exception):
    """raise this when no connection is found"""

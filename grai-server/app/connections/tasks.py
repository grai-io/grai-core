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

        if connector.name == "postgres":
            run_postgres()
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


def run_postgres():
    pass


class NoConnectorError(Exception):
    """raise this when no connection is found"""

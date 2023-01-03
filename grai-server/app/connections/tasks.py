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
    from grai_client.endpoints.v1.client import ClientV1

    # client = ClientV1('pr63.api.grai.io', '443')
    client = ClientV1('localhost', '8000', workspace="198e90f3-112e-4a11-84e7-1b5a4f02cec1")
    client.set_authentication_headers(username='null@grai.io', password='super_secret')
    # client.set_authentication_headers(api_key='qBzzVcCT.sVPZ3yVrv4e7oA9yzEtdrc1HwAOmLlsa')
    # client.set_authentication_headers(api_key='PYqPIzQp.06JTpWid4V0JN0wEkEVqo2Bcq3gHSUig')

    from grai_source_postgres.base import update_server

    update_server(client, dbname="grai", user='grai', password='grai', namespace='test')



class NoConnectorError(Exception):
    """raise this when no connection is found"""

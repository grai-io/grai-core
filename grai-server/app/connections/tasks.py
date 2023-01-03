from .models import Run
from celery import shared_task
from datetime import datetime


@shared_task
def add(x, y):
    print("Hello task running")
    print(x + y)
    # return x + y


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
        run.status = "success"
        run.finished = datetime.now()
        run.save()
    except Exception as e:
        run.metadata = e
        run.status = "error"
        run.finished = datetime.now()
        run.save()

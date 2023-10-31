import os
from datetime import timedelta
from celery import Celery

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "the_guide.settings.celery")

app = Celery("the_guide")

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object("django.conf:settings", namespace="CELERY")

app.conf.beat_schedule = {
    "lineage:Node:bulk_update_embeddings": {
        "task": "lineage.tasks.bulk_update_embeddings",
        "schedule": timedelta(minutes=5),
    },
}

# Load task modules from all registered Django apps.
app.autodiscover_tasks()

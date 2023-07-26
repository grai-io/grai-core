# This will make sure the app is always imported when
# Django starts so that shared_task will use this app.
from .celery import app as celery_app

__version__ = "0.1.36"
__all__ = ("celery_app",)

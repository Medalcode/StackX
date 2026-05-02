from .celery_app import celery
from . import sanity_sync


@celery.task(bind=True, name='backend.app.tasks.sync_sanity',
             max_retries=3, default_retry_delay=60)
def sync_sanity(self):
    """Celery task that executes sanity_sync.sync().

    Retries up to 3 times with a 60-second delay on failure.
    """
    try:
        sanity_sync.sync()
    except Exception as exc:
        raise self.retry(exc=exc)

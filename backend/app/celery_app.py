import os
from celery import Celery

REDIS_URL = os.getenv('REDIS_URL', 'redis://redis:6379/0')

celery = Celery(
    'stackx',
    broker=REDIS_URL,
    backend=REDIS_URL,
    include=['backend.app.tasks'],
)

celery.conf.update(
    task_serializer='json',
    result_serializer='json',
    accept_content=['json'],
    timezone='UTC',
    enable_utc=True,
)

# ---------------------------------------------------------------------------
# Celery Beat schedule – periodic Sanity/GROQ sync
# ---------------------------------------------------------------------------
SYNC_INTERVAL = int(os.getenv('SYNC_INTERVAL_SECONDS', '3600'))

celery.conf.beat_schedule = {
    'sanity-sync-periodic': {
        'task': 'backend.app.tasks.sync_sanity',
        'schedule': SYNC_INTERVAL,
    },
}

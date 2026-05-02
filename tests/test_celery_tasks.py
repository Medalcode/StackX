"""Tests for Celery task wiring.

These tests verify that the sync_sanity task is properly registered
in the Celery app without requiring a live Redis/worker connection.
"""
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


def test_sync_sanity_task_registered():
    """sync_sanity task should be registered in the Celery app."""
    # Import tasks module to ensure tasks are registered
    import backend.app.tasks  # noqa: F401
    from backend.app.celery_app import celery
    assert 'backend.app.tasks.sync_sanity' in celery.tasks


def test_sync_sanity_task_is_callable():
    """sync_sanity task should be importable and callable (signature check)."""
    from backend.app.tasks import sync_sanity
    # The task is a Celery Task instance with a delay() method
    assert callable(getattr(sync_sanity, 'delay', None))


def test_celery_beat_schedule_uses_sync_interval():
    """Celery Beat schedule should use SYNC_INTERVAL_SECONDS from env."""
    from unittest.mock import patch
    import importlib
    import backend.app.celery_app as celery_mod

    with patch.dict(os.environ, {'SYNC_INTERVAL_SECONDS': '1800'}):
        importlib.reload(celery_mod)

    schedule = celery_mod.celery.conf.beat_schedule
    assert 'sanity-sync-periodic' in schedule
    entry = schedule['sanity-sync-periodic']
    assert entry['task'] == 'backend.app.tasks.sync_sanity'
    assert entry['schedule'] == 1800

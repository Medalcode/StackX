"""Tests for Sanity/GROQ sync module."""

import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest

from backend.app import sanity_sync
from backend.app.models import Category, Technology


def test_fetch_technologies_without_project_id(monkeypatch):
    monkeypatch.delenv("SANITY_PROJECT_ID", raising=False)
    with pytest.raises(RuntimeError, match="SANITY_PROJECT_ID not set"):
        sanity_sync.fetch_technologies()


def test_upsert_technologies_db(db_session):
    techs_payload = [
        {
            "_id": "tech-1",
            "name": "Vue.js",
            "description": "Progressive JS Framework",
            "category": {"name": "Frontend"},
        },
        {
            "_id": "tech-2",
            "name": "FastAPI",
            "description": "Updated FastAPI Description",
            "category": {"name": "Backend"},
        },
    ]

    sanity_sync.upsert_technologies(db_session, techs_payload)

    # Verify category creation
    cat = db_session.query(Category).filter_by(name="Frontend").first()
    assert cat is not None

    # Verify technology creation
    vue = db_session.query(Technology).filter_by(name="Vue.js").first()
    assert vue is not None
    assert vue.description == "Progressive JS Framework"
    assert vue.category_id == cat.id

    # Verify technology update (FastAPI existed in seed data)
    fastapi = db_session.query(Technology).filter_by(name="FastAPI").first()
    assert fastapi is not None
    assert fastapi.description == "Updated FastAPI Description"

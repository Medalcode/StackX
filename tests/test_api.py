"""Tests for API routes."""

import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


import pytest


@pytest.mark.smoke
def test_health_endpoint(client):
    resp = client.get("/health")
    assert resp.status_code == 200
    data = resp.json()
    assert data["status"] == "ok"


@pytest.mark.smoke
@pytest.mark.integration
def test_recommend_endpoint(client):
    resp = client.post("/recommend-stack/", json={
        "weights": {"Escalabilidad": 0.9, "Facilidad": 0.5},
        "proyecto": "Test",
    })
    assert resp.status_code == 200
    data = resp.json()
    assert "recommendations" in data
    assert len(data["recommendations"]) > 0
    for r in data["recommendations"]:
        assert "name" in r
        assert "final_score" in r
        assert "justification" in r


@pytest.mark.integration
def test_recommend_endpoint_with_project(client):
    resp = client.post("/recommend-stack/", json={
        "weights": {"Escalabilidad": 1.0},
        "proyecto": "Mi SaaS",
    })
    assert resp.status_code == 200
    data = resp.json()
    assert len(data["recommendations"]) > 0


@pytest.mark.integration
def test_recommend_endpoint_with_justification_skill_header(client):
    resp = client.post(
        "/recommend-stack/",
        json={"weights": {"Escalabilidad": 0.8}},
        headers={"X-Justification-Skill": "content_generator"},
    )
    assert resp.status_code == 200
    data = resp.json()
    assert len(data["recommendations"]) > 0


@pytest.mark.integration
def test_recommend_get_paginated_endpoint(client):
    weights_json = '{"Escalabilidad": 0.9}'
    resp = client.get(f'/recommend-stack/?weights={weights_json}&skip=0&limit=2')
    assert resp.status_code == 200
    data = resp.json()
    assert "recommendations" in data
    assert data["skip"] == 0
    assert data["limit"] == 2


@pytest.mark.integration
def test_admin_sync_no_token(client):
    resp = client.post("/admin/sync-groq/")
    assert resp.status_code == 403


@pytest.mark.integration
def test_admin_sync_wrong_token(client):
    resp = client.post(
        "/admin/sync-groq/",
        headers={"Authorization": "Bearer wrong_token"},
    )
    assert resp.status_code == 403


@pytest.mark.integration
def test_admin_sync_valid_token_bearer(client, monkeypatch):
    monkeypatch.setenv("ADMIN_TOKEN", "secret123")
    resp = client.post(
        "/admin/sync-groq/",
        headers={"Authorization": "Bearer secret123"},
    )
    assert resp.status_code == 200
    data = resp.json()
    assert data["status"] == "accepted"


@pytest.mark.integration
def test_admin_sync_valid_token_header(client, monkeypatch):
    monkeypatch.setenv("ADMIN_TOKEN", "secret123")
    resp = client.post(
        "/admin/sync-groq/",
        headers={"X-ADMIN-TOKEN": "secret123"},
    )
    assert resp.status_code == 200
    data = resp.json()
    assert data["status"] == "accepted"


@pytest.mark.integration
def test_recommend_export_markdown_endpoint(client):
    resp = client.post(
        "/recommend-stack/export-markdown/",
        json={"weights": {"Escalabilidad": 0.9}, "proyecto": "SaaS Demo"},
    )
    assert resp.status_code == 200
    assert "text/markdown" in resp.headers["content-type"]
    text = resp.text
    assert "# Dictamen Técnico de Arquitectura — SaaS Demo" in text
    assert "## Stacks Recomendados" in text


@pytest.mark.integration
def test_favorites_endpoints(client):
    post_resp = client.post(
        "/recommend-stack/favorites/?name=Mi%20Stack%20Fav",
        json={"weights": {"Escalabilidad": 0.95}, "proyecto": "Fav Project"},
    )
    assert post_resp.status_code == 200
    data = post_resp.json()
    assert data["name"] == "Mi Stack Fav"
    assert data["proyecto"] == "Fav Project"

    get_resp = client.get("/recommend-stack/favorites/")
    assert get_resp.status_code == 200
    favs = get_resp.json()
    assert len(favs) > 0




"""Tests for API routes."""

import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


def test_health_endpoint(client):
    resp = client.get("/health")
    assert resp.status_code == 200
    data = resp.json()
    assert data["status"] == "ok"


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


def test_recommend_endpoint_with_project(client):
    resp = client.post("/recommend-stack/", json={
        "weights": {"Escalabilidad": 1.0},
        "proyecto": "Mi SaaS",
    })
    assert resp.status_code == 200
    data = resp.json()
    assert len(data["recommendations"]) > 0


def test_recommend_endpoint_with_justification_skill_header(client):
    resp = client.post(
        "/recommend-stack/",
        json={"weights": {"Escalabilidad": 0.8}},
        headers={"X-Justification-Skill": "content_generator"},
    )
    assert resp.status_code == 200
    data = resp.json()
    assert len(data["recommendations"]) > 0


def test_admin_sync_no_token(client):
    resp = client.post("/admin/sync-groq/")
    assert resp.status_code == 403


def test_admin_sync_wrong_token(client):
    resp = client.post(
        "/admin/sync-groq/",
        headers={"Authorization": "Bearer wrong_token"},
    )
    assert resp.status_code == 403

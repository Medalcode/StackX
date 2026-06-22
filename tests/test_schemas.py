"""Tests for Pydantic schemas."""

import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


def test_user_weights_valid():
    from backend.app.schemas import UserWeights
    payload = UserWeights(weights={"Escalabilidad": 0.9}, proyecto="MVP")
    assert payload.weights["Escalabilidad"] == 0.9
    assert payload.proyecto == "MVP"


def test_user_weights_without_project():
    from backend.app.schemas import UserWeights
    payload = UserWeights(weights={"Facilidad": 0.5})
    assert payload.proyecto is None


def test_recommendation_item():
    from backend.app.schemas import RecommendationItem
    item = RecommendationItem(
        name="FastAPI",
        category="Backend",
        final_score=8.5,
        justification="Great framework",
        team_suggestion=[{"role": "Dev", "count": 1}],
    )
    assert item.name == "FastAPI"
    assert item.final_score == 8.5


def test_recommendation_item_minimal():
    from backend.app.schemas import RecommendationItem
    item = RecommendationItem(name="Go", category=None, final_score=7.0)
    assert item.justification is None
    assert item.team_suggestion is None


def test_recommendation_response():
    from backend.app.schemas import RecommendationItem, RecommendationResponse
    items = [
        RecommendationItem(name="A", category=None, final_score=1.0),
        RecommendationItem(name="B", category=None, final_score=2.0),
    ]
    resp = RecommendationResponse(recommendations=items)
    assert len(resp.recommendations) == 2


def test_paginated_response():
    from backend.app.schemas import PaginatedRecommendationResponse, RecommendationItem
    items = [
        RecommendationItem(name="A", category=None, final_score=1.0),
    ]
    resp = PaginatedRecommendationResponse(recommendations=items, skip=0, limit=10)
    assert resp.skip == 0
    assert resp.limit == 10

"""Tests for recommendation service layer."""

import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest

from backend.app.schemas import UserWeights
from backend.app.services import recommendation_service


@pytest.mark.asyncio
async def test_get_stack_recommendations_service(db_session):
    payload = UserWeights(weights={"Escalabilidad": 0.9, "Facilidad": 0.5}, proyecto="Service Test")
    response = await recommendation_service.get_stack_recommendations(db_session, payload, top_n=2)

    assert len(response.recommendations) <= 2
    assert len(response.recommendations) > 0
    for rec in response.recommendations:
        assert rec.name is not None
        assert rec.final_score > 0
        assert rec.justification is not None
        assert rec.team_suggestion is not None


@pytest.mark.asyncio
async def test_get_paginated_stack_recommendations_service(db_session):
    user_weights = {"Escalabilidad": 1.0}
    response = await recommendation_service.get_paginated_stack_recommendations(
        db_session, user_weights, proyecto="Pagination Test", skip=0, limit=2
    )

    assert len(response.recommendations) <= 2
    assert response.skip == 0
    assert response.limit == 2
    for rec in response.recommendations:
        assert rec.name is not None
        assert rec.final_score > 0
        assert rec.justification is not None

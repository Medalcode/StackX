"""Tests for the recommendation engine."""

import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


def test_calculate_score(db_session):
    from backend.app.models import Technology
    from backend.app.recommender import calculate_score_for_tech

    tech = db_session.query(Technology).filter_by(name="FastAPI").first()
    assert tech is not None

    score = calculate_score_for_tech(tech, {"Escalabilidad": 1.0})
    assert score > 0


def test_calculate_score_empty_weights(db_session):
    from backend.app.models import Technology
    from backend.app.recommender import calculate_score_for_tech

    tech = db_session.query(Technology).filter_by(name="FastAPI").first()
    score = calculate_score_for_tech(tech, {})
    assert score == 0.0


def test_get_recommendations(db_session):
    from backend.app.recommender import get_recommendations

    results = get_recommendations(db_session, {"Escalabilidad": 1.0}, top_n=2)
    assert len(results) <= 2
    assert all(r["final_score"] > 0 for r in results)


def test_get_recommendations_ordering(db_session):
    from backend.app.recommender import get_recommendations

    results = get_recommendations(db_session, {"Escalabilidad": 1.0}, top_n=3)
    scores = [r["final_score"] for r in results]
    assert scores == sorted(scores, reverse=True)


def test_get_recommendations_with_multiple_weights(db_session):
    from backend.app.recommender import get_recommendations

    results = get_recommendations(
        db_session,
        {"Escalabilidad": 0.9, "Facilidad": 0.5, "Ecosistema": 0.3},
        top_n=3,
    )
    assert len(results) == 3
    assert all(r.get("category") is not None for r in results)


def test_get_recommendations_paginated(db_session):
    from backend.app.recommender import get_recommendations_paginated

    page1 = get_recommendations_paginated(db_session, {"Escalabilidad": 1.0}, skip=0, limit=2)
    assert len(page1) <= 2

    page2 = get_recommendations_paginated(db_session, {"Escalabilidad": 1.0}, skip=2, limit=2)
    assert len(page2) <= 2

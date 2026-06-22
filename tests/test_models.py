"""Tests for SQLAlchemy models."""

import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


def test_create_category(db_session):
    from backend.app.models import Category
    cat = Category(name="Test", description="Test category")
    db_session.add(cat)
    db_session.commit()
    assert cat.id is not None


def test_create_technology(db_session):
    from backend.app.models import Category, Technology
    cat = Category(name="TestCat")
    db_session.add(cat)
    db_session.commit()

    tech = Technology(name="TestTech", description="A test", category_id=cat.id)
    db_session.add(tech)
    db_session.commit()
    assert tech.id is not None
    assert tech.category.name == "TestCat"


def test_create_attribute_and_score(db_session):
    from backend.app.models import Attribute, Category, Technology, TechScore
    cat = Category(name="TestCat")
    db_session.add(cat)
    db_session.commit()

    tech = Technology(name="TestTech", category_id=cat.id)
    db_session.add(tech)
    attr = Attribute(name="Performance")
    db_session.add(attr)
    db_session.commit()

    score = TechScore(tech_id=tech.id, attr_id=attr.id, value=9.5)
    db_session.add(score)
    db_session.commit()

    assert score.id is not None
    db_session.refresh(tech)
    assert len(tech.scores) == 1
    assert tech.scores[0].value == 9.5


def test_unique_technology_name(db_session):
    import pytest
    from sqlalchemy.exc import IntegrityError

    from backend.app.models import Technology

    tech1 = Technology(name="Unique")
    db_session.add(tech1)
    db_session.commit()

    tech2 = Technology(name="Unique")
    db_session.add(tech2)
    with pytest.raises(IntegrityError):
        db_session.commit()
    db_session.rollback()

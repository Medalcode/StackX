from sqlalchemy.orm import Session, joinedload

from .models import Technology, TechScore


def calculate_score_for_tech(tech: Technology, user_weights: dict[str, float]) -> float:
    total_weights = sum(user_weights.values()) if user_weights else 0.0
    if total_weights <= 0:
        return 0.0

    total_score = 0.0
    for score in tech.scores:
        attr_name = score.attribute.name
        if attr_name in user_weights:
            total_score += score.value * user_weights[attr_name]

    return total_score / total_weights


def get_recommendations(db: Session, user_weights: dict[str, float], top_n: int = 3) -> list[dict]:
    technologies = (
        db.query(Technology)
        .options(joinedload(Technology.scores).joinedload(TechScore.attribute))
        .options(joinedload(Technology.category))
        .all()
    )
    results = []

    for tech in technologies:
        final_score = calculate_score_for_tech(tech, user_weights)
        results.append({
            'name': tech.name,
            'final_score': round(final_score, 3),
            'category': tech.category.name if tech.category else None,
            'tech_id': tech.id,
        })

    recommendations = sorted(results, key=lambda x: x['final_score'], reverse=True)
    return recommendations[:top_n]


def get_recommendations_paginated(
    db: Session, user_weights: dict[str, float],
    skip: int = 0, limit: int = 10
) -> list[dict]:
    technologies = (
        db.query(Technology)
        .options(joinedload(Technology.scores).joinedload(TechScore.attribute))
        .options(joinedload(Technology.category))
        .offset(skip)
        .limit(limit)
        .all()
    )
    results = []

    for tech in technologies:
        final_score = calculate_score_for_tech(tech, user_weights)
        results.append({
            'name': tech.name,
            'final_score': round(final_score, 3),
            'category': tech.category.name if tech.category else None,
            'tech_id': tech.id,
        })

    return sorted(results, key=lambda x: x['final_score'], reverse=True)

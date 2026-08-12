import asyncio

from sqlalchemy.orm import Session

from .. import ai_client, recommender
from ..schemas import (
    PaginatedRecommendationResponse,
    RecommendationItem,
    RecommendationResponse,
    UserWeights,
)

DEFAULT_TEAM_SUGGESTION = [
    {"role": "Backend Dev", "count": 1},
    {"role": "Frontend Dev", "count": 1},
]


async def get_stack_recommendations(
    db: Session,
    payload: UserWeights,
    justification_skill: str | None = None,
    top_n: int = 3,
) -> RecommendationResponse:
    user_weights = payload.weights
    projects = recommender.get_recommendations(db, user_weights, top_n=top_n)

    tasks = [
        ai_client.generate_justification(payload.model_dump(), item, skill_name=justification_skill)
        for item in projects
    ]
    justifications = await asyncio.gather(*tasks)

    results = []
    for item, justification in zip(projects, justifications, strict=True):
        results.append(
            RecommendationItem(
                name=item["name"],
                category=item.get("category"),
                final_score=item["final_score"],
                justification=justification,
                team_suggestion=DEFAULT_TEAM_SUGGESTION,
            )
        )

    return RecommendationResponse(recommendations=results)


async def get_paginated_stack_recommendations(
    db: Session,
    user_weights: dict[str, float],
    proyecto: str | None = None,
    skip: int = 0,
    limit: int = 10,
) -> PaginatedRecommendationResponse:
    payload = UserWeights(weights=user_weights, proyecto=proyecto)
    projects = recommender.get_recommendations_paginated(db, user_weights, skip=skip, limit=limit)

    tasks = [
        ai_client.generate_justification(payload.model_dump(), item)
        for item in projects
    ]
    justifications = await asyncio.gather(*tasks)

    results = []
    for item, justification in zip(projects, justifications, strict=True):
        results.append(
            RecommendationItem(
                name=item["name"],
                category=item.get("category"),
                final_score=item["final_score"],
                justification=justification,
            )
        )

    return PaginatedRecommendationResponse(
        recommendations=results,
        skip=skip,
        limit=limit,
    )

import asyncio

from fastapi import APIRouter, Depends, Header, Query
from sqlalchemy.orm import Session

from .. import ai_client, recommender
from ..database import get_db
from ..schemas import (
    PaginatedRecommendationResponse,
    RecommendationItem,
    RecommendationResponse,
    UserWeights,
)

router = APIRouter()


@router.post('/recommend-stack/', response_model=RecommendationResponse)
async def recommend_stack(
    payload: UserWeights,
    db: Session = Depends(get_db),  # noqa: B008
    justification_skill: str | None = Header(None, alias="X-Justification-Skill"),
):
    user_weights = payload.weights
    projects = recommender.get_recommendations(db, user_weights, top_n=3)

    tasks = [
        ai_client.generate_justification(payload.model_dump(), item, skill_name=justification_skill)
        for item in projects
    ]

    justifications = await asyncio.gather(*tasks)

    results = []
    for item, justification in zip(projects, justifications, strict=True):
        team = [
            {"role": "Backend Dev", "count": 1},
            {"role": "Frontend Dev", "count": 1},
        ]
        results.append(RecommendationItem(
            name=item['name'],
            category=item.get('category'),
            final_score=item['final_score'],
            justification=justification,
            team_suggestion=team,
        ))

    return RecommendationResponse(recommendations=results)


@router.get('/recommend-stack/', response_model=PaginatedRecommendationResponse)
async def recommend_stack_paginated(
    weights: str = Query(description='JSON weights, e.g. {"Escalabilidad":0.9}'),
    proyecto: str | None = Query(None),
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db),  # noqa: B008
):
    import json
    user_weights = json.loads(weights)
    payload = UserWeights(weights=user_weights, proyecto=proyecto)
    projects = recommender.get_recommendations_paginated(db, user_weights, skip=skip, limit=limit)

    tasks = [
        ai_client.generate_justification(payload.model_dump(), item)
        for item in projects
    ]

    justifications = await asyncio.gather(*tasks)

    results = []
    for item, justification in zip(projects, justifications, strict=True):
        results.append(RecommendationItem(
            name=item['name'],
            category=item.get('category'),
            final_score=item['final_score'],
            justification=justification,
        ))

    return PaginatedRecommendationResponse(
        recommendations=results,
        skip=skip,
        limit=limit,
    )

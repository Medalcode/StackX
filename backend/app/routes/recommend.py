import json

from fastapi import APIRouter, Depends, Header, Query
from sqlalchemy.orm import Session

from ..database import get_db
from ..schemas import (
    PaginatedRecommendationResponse,
    RecommendationResponse,
    UserWeights,
)
from ..services import recommendation_service

router = APIRouter()


@router.post('/recommend-stack/', response_model=RecommendationResponse)
async def recommend_stack(
    payload: UserWeights,
    db: Session = Depends(get_db),  # noqa: B008
    justification_skill: str | None = Header(None, alias="X-Justification-Skill"),
):
    return await recommendation_service.get_stack_recommendations(
        db, payload, justification_skill=justification_skill
    )


@router.get('/recommend-stack/', response_model=PaginatedRecommendationResponse)
async def recommend_stack_paginated(
    weights: str = Query(description='JSON weights, e.g. {"Escalabilidad":0.9}'),
    proyecto: str | None = Query(None),
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db),  # noqa: B008
):
    user_weights = json.loads(weights)
    return await recommendation_service.get_paginated_stack_recommendations(
        db, user_weights, proyecto=proyecto, skip=skip, limit=limit
    )


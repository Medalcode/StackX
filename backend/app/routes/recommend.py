import json

from fastapi import APIRouter, Depends, Header, Query, Request, Response
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
    request: Request,  # noqa: ARG001
    payload: UserWeights,
    db: Session = Depends(get_db),  # noqa: B008
    justification_skill: str | None = Header(None, alias="X-Justification-Skill"),
):
    return await recommendation_service.get_stack_recommendations(
        db, payload, justification_skill=justification_skill
    )


@router.post('/recommend-stack/export-markdown/', response_class=Response)
async def export_recommend_stack_markdown(
    request: Request,  # noqa: ARG001
    payload: UserWeights,
    db: Session = Depends(get_db),  # noqa: B008
    justification_skill: str | None = Header(None, alias="X-Justification-Skill"),
):
    md_content = await recommendation_service.export_stack_recommendations_markdown(
        db, payload, justification_skill=justification_skill
    )
    return Response(content=md_content, media_type="text/markdown")


@router.get('/recommend-stack/', response_model=PaginatedRecommendationResponse)
async def recommend_stack_paginated(
    request: Request,  # noqa: ARG001
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


@router.post('/recommend-stack/favorites/')
def create_favorite(payload: UserWeights, name: str | None = Query(None)):
    return recommendation_service.add_favorite_stack(payload, name=name)


@router.get('/recommend-stack/favorites/')
def list_favorites():
    return recommendation_service.get_favorite_stacks()




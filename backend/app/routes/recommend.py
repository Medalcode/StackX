import asyncio
from fastapi import APIRouter, Depends, Header
from sqlalchemy.orm import Session

from .. import ai_client, recommender
from ..database import get_db
from ..schemas import RecommendationItem, RecommendationResponse, UserWeights

router = APIRouter()


@router.post('/recommend-stack/', response_model=RecommendationResponse)
async def recommend_stack(payload: UserWeights, db: Session = Depends(get_db), justification_skill: str | None = Header(None, alias="X-Justification-Skill")):
    user_weights = payload.weights
    projects = recommender.get_recommendations(db, user_weights, top_n=3)
    
    tasks = [
        ai_client.generate_justification(payload.model_dump(), item, skill_name=justification_skill)
        for item in projects
    ]
    
    justifications = await asyncio.gather(*tasks)

    results = []
    for item, justification in zip(projects, justifications):
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

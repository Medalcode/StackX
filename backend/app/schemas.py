from typing import Any

from pydantic import BaseModel


class UserWeights(BaseModel):
    weights: dict[str, float]
    proyecto: str | None = None


class RecommendationItem(BaseModel):
    name: str
    category: str | None
    final_score: float
    justification: str | None = None
    team_suggestion: list[dict[str, Any]] | None = None


class RecommendationResponse(BaseModel):
    recommendations: list[RecommendationItem]


class PaginatedRecommendationResponse(BaseModel):
    recommendations: list[RecommendationItem]
    skip: int
    limit: int

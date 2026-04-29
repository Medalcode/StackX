from typing import Any

from pydantic import BaseModel


class UserWeights(BaseModel):
    # e.g. {"Escalabilidad": 0.9, "Facilidad": 0.5}
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

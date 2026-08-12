import asyncio
import hashlib
import time

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


class RecommendationCache:
    def __init__(self, ttl_seconds: int = 300, max_size: int = 200):
        self.ttl_seconds = ttl_seconds
        self.max_size = max_size
        self._store: dict[str, tuple[float, RecommendationResponse]] = {}

    def _make_key(self, payload: UserWeights, justification_skill: str | None, top_n: int) -> str:
        sorted_weights = sorted(payload.weights.items()) if payload.weights else []
        raw_key = f"{sorted_weights}:{payload.proyecto}:{justification_skill}:{top_n}"
        return hashlib.sha256(raw_key.encode("utf-8")).hexdigest()

    def get(
        self, payload: UserWeights, justification_skill: str | None, top_n: int
    ) -> RecommendationResponse | None:
        key = self._make_key(payload, justification_skill, top_n)
        entry = self._store.get(key)
        if not entry:
            return None
        created_at, response = entry
        if time.time() - created_at > self.ttl_seconds:
            del self._store[key]
            return None
        return response

    def set(
        self,
        payload: UserWeights,
        justification_skill: str | None,
        top_n: int,
        response: RecommendationResponse,
    ) -> None:
        if len(self._store) >= self.max_size:
            self._store.clear()
        key = self._make_key(payload, justification_skill, top_n)
        self._store[key] = (time.time(), response)

    def clear(self) -> None:
        self._store.clear()


cache = RecommendationCache()


async def get_stack_recommendations(
    db: Session,
    payload: UserWeights,
    justification_skill: str | None = None,
    top_n: int = 3,
) -> RecommendationResponse:
    cached_response = cache.get(payload, justification_skill, top_n)
    if cached_response is not None:
        return cached_response

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

    response = RecommendationResponse(recommendations=results)
    cache.set(payload, justification_skill, top_n, response)
    return response



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


async def export_stack_recommendations_markdown(
    db: Session,
    payload: UserWeights,
    justification_skill: str | None = None,
    top_n: int = 3,
) -> str:
    response = await get_stack_recommendations(
        db, payload, justification_skill=justification_skill, top_n=top_n
    )
    proyecto_name = payload.proyecto or "Proyecto SaaS"

    lines = [
        f"# Dictamen Técnico de Arquitectura — {proyecto_name}",
        "",
        "## Prioridades del Usuario",
    ]
    for attr, val in payload.weights.items():
        lines.append(f"- **{attr}**: {val}")
    lines.append("")

    lines.append("## Stacks Recomendados")
    for idx, item in enumerate(response.recommendations, 1):
        lines.append(f"### {idx}. {item.name} (Score: {item.final_score})")
        if item.category:
            lines.append(f"**Categoría:** {item.category}")
        lines.append("")
        lines.append("#### Justificación & Trade-offs")
        lines.append(item.justification or "Sin justificación detallada.")
        lines.append("")
        if item.team_suggestion:
            lines.append("#### Sugerencia de Equipo")
            for t in item.team_suggestion:
                lines.append(f"- {t.get('role', 'Dev')}: {t.get('count', 1)}")
            lines.append("")

    return "\n".join(lines)


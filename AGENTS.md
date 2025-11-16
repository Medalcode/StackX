# StackX — Agent Guide

## Commands
```bash
# Backend:
pip install -r backend/requirements.txt
uvicorn backend.app.main:app --reload              # API on :8000

# Frontend (Next.js):
cd frontend && npm install && npm run dev          # UI on :3000

# Docker (everything):
docker-compose up --build                          # Postgres + backend + frontend

# Tests:
pytest -q tests/                                   # 2 tests (LLM fallback)

# Seed data:
python -c "from backend.app.database import SessionLocal; from backend.app.seed_data import seed; db = next(SessionLocal()); seed(db)"
```

## Critical Quirks

- **Full-stack**: Python FastAPI backend + JavaScript Next.js frontend. Both must run for the app to work. Don't modify one without checking the other.
- **Pydantic V2 critical**: `payload.dict()` will fail — use `payload.model_dump()` instead. This is a known migration gotcha (see BITACORA.md).
- **LLM fallback**: Ollama integration (`backend/app/ai_client.py`) is optional. If `OLLAMA_URL` is unreachable, the system returns a template-based justification instead of an LLM-generated one. Tests verify this fallback behavior.
- **Sanity/GROQ sync** is optional (`backend/app/sanity_sync.py`). Activated only when `SANITY_PROJECT_ID` env var is set. Without it, the `/admin/sync-groq/` endpoint returns an error.
- **No auth on recommend endpoint**: `/recommend-stack/` is public. Only `/admin/sync-groq/` is protected by `ADMIN_TOKEN`.
- **Test quirks**: only 2 tests exist, in `tests/test_skill_contract.py`. Tests modify `sys.path` at import. Run `pytest -q tests/` from repo root.
- **APScheduler** runs in-process — for production with multiple replicas, externalize to Celery/RQ with Redis.
- **`.env.example`** has the key env vars. Copy to `.env` and configure `OLLAMA_URL` if using LLM features.

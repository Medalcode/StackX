# Stack Recommender (prototype)

Backend prototype with FastAPI, SQLAlchemy and a simple recommender engine.

Run locally:

```bash
python -m pip install -r backend/requirements.txt
uvicorn backend.app.main:app --reload
```

The server will create a local SQLite DB at `dev.db`. To seed sample data, run a short script (use Python REPL):

```py
from backend.app.database import SessionLocal
from backend.app.seed_data import seed
db = next(SessionLocal())
seed(db)
```

Admin sync endpoint
-------------------

Trigger a GROQ/Sanity sync via the admin endpoint (runs in background). If you want to protect this endpoint, set `ADMIN_TOKEN` in your environment and provide it with the request either as an `Authorization: Bearer <token>` header or `X-ADMIN-TOKEN: <token>`.

Example:

```bash
curl -X POST "http://localhost:8000/admin/sync-groq/" -H "Authorization: Bearer your_admin_token_here"
```

Bitácora
-------

Se añadió `BITACORA.md` en la raíz del proyecto con un registro de tareas realizadas y pendientes, instrucciones de ejecución y notas de seguridad.
Periodic sync
-------------

If you set `SANITY_PROJECT_ID`, the app will run an immediate sync at startup and schedule periodic syncs every `SYNC_INTERVAL_SECONDS` (default 3600). You can adjust `SYNC_INTERVAL_SECONDS` in your environment.

Recent additions
----------------

- `docs/agent.md` and `docs/skills.md`: design and operational documentation for the agent and skills architecture.
- `backend/app/ai_skills/example_skill.py`: example skill implementing the `run_skill(input: dict) -> dict` contract.
- `backend/app/skills_registry.py`: dynamic loader/registry for skills under `backend/app/ai_skills/`.
- `backend/app/ai_client.py` updated to attempt executing a registered skill (env `JUSTIFICATION_SKILL` or first available) before calling the LLM; also respects `OLLAMA_TIMEOUT`.
- `tests/test_skill_contract.py`: contract test asserting that `example_skill` integrates with `ai_client`.

How to run the new contract test locally:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r backend/requirements.txt
pip install pytest
pytest -q tests/test_skill_contract.py
```

Notes
-----

- I added a `.gitignore` to avoid committing `.venv` and other Python artifacts. If you already committed a virtual environment, consider removing it from the repo and keeping the `.gitignore`.
- The scheduler currently uses an in-process `APScheduler`. For production scaling we recommend leader-election via Redis or externalizing periodic work to a worker queue — see `docs/agent.md` for details.



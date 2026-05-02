# StackX — Recomendador de Stack Tecnológico

Backend con FastAPI, SQLAlchemy y un motor de recomendación por pesos ponderados. Incluye integración opcional con LLM (Ollama) y Sanity/GROQ para gestión de contenido.

---

## Arquitectura

La arquitectura sigue el principio de **agentes versátiles + super-skills paramétricas**. Ver detalles en [`docs/agents.md`](docs/agents.md) y [`docs/skills.md`](docs/skills.md).

### Componentes del sistema

```
┌─────────────┐    enqueue     ┌────────────┐     ┌──────────────────┐
│  FastAPI    │ ─────────────► │   Redis    │ ◄── │  Celery Beat     │
│  (backend)  │                │  (broker)  │     │  (periodic sync) │
└─────────────┘                └────────────┘     └──────────────────┘
                                     │
                                     ▼
                               ┌────────────┐
                               │   Celery   │
                               │  Worker(s) │
                               └────────────┘
                                     │
                                     ▼
                               ┌────────────┐
                               │  Postgres  │
                               └────────────┘
```

- **backend** – FastAPI web process (stateless; no schedulers inside the process).
- **redis** – Message broker and Celery result backend.
- **worker** – Celery worker that executes background tasks (e.g. `sync_sanity`).
- **beat** – Celery Beat scheduler that enqueues the periodic sync every `SYNC_INTERVAL_SECONDS`.

### Agentes
| Agente | Rol | Skills asociadas |
|---|---|---|
| `ArchitectAgent` | Orquesta recomendación y justificación | `content_generator`, `data_analysis` |
| `DataAgent` | Sincronización y curación de datos | `sanity_sync` |

### Skills activas (`backend/app/ai_skills/`)
| Skill | Parámetro clave | Reemplaza a |
|---|---|---|
| `content_generator` | `mode`: `full_justification \| concise_summary \| technical_comparison` | `example_skill` (eliminada) |
| `data_analysis` | `operation`: `calculate_stack_score \| validate_compatibility \| enrich_metadata` | skills individuales de scoring |

---

## Ejecución local

### Backend

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r backend/requirements.txt
uvicorn backend.app.main:app --reload
```

El servidor levanta en `http://localhost:8000` y crea una base de datos SQLite en `dev.db`.

### Sembrar datos de ejemplo

```python
from backend.app.database import SessionLocal
from backend.app.seed_data import seed
db = next(SessionLocal())
seed(db)
```

### Frontend (Next.js)

```bash
cd frontend
npm install
npm run dev
```

### Docker Compose (todo junto)

```bash
cp .env.example .env   # editar las variables necesarias
docker-compose up --build
```

Esto levanta:
- `db` – Postgres 15
- `redis` – Redis 7
- `backend` – FastAPI en `:8000`
- `worker` – Celery worker
- `beat` – Celery Beat (agenda el sync periódico)
- `frontend` – Next.js en `:3000`

Para escalar workers: `docker-compose up --scale worker=3`

---

## Variables de entorno

| Variable | Default | Descripción |
|---|---|---|
| `DATABASE_URL` | `sqlite:///./dev.db` | URL de la base de datos |
| `REDIS_URL` | `redis://redis:6379/0` | URL del broker Redis |
| `OLLAMA_URL` | — | Endpoint del LLM (ej: `http://localhost:11434/v1/generate`) |
| `OLLAMA_TIMEOUT` | `10` | Timeout en segundos para llamadas al LLM |
| `JUSTIFICATION_SKILL` | — | Nombre de la skill a usar (`content_generator`, etc.) |
| `SANITY_PROJECT_ID` | — | ID del proyecto Sanity (activa sincronización) |
| `SANITY_DATASET` | `production` | Dataset de Sanity |
| `SANITY_TOKEN` | — | Token de autenticación Sanity |
| `SYNC_INTERVAL_SECONDS` | `3600` | Frecuencia de sincronización periódica (en segundos) |
| `ADMIN_TOKEN` | — | Token para proteger el endpoint `/admin/sync-groq/` |

Copia `.env.example` a `.env` y configura los valores necesarios.

---

## Endpoints principales

### `POST /recommend-stack/`
Devuelve el top-3 de stacks recomendados según los pesos del usuario.

```bash
curl -X POST http://localhost:8000/recommend-stack/ \
  -H "Content-Type: application/json" \
  -d '{"weights": {"Escalabilidad": 0.9, "Facilidad": 0.5}, "proyecto": "Mi SaaS"}'
```

Header opcional `X-Justification-Skill: content_generator` para seleccionar skill explícita.

### `POST /admin/sync-groq/`
Encola un job de sincronización Sanity/GROQ en Celery y devuelve el `job_id`.

```bash
curl -X POST http://localhost:8000/admin/sync-groq/ \
  -H "Authorization: Bearer your_admin_token_here"
```

Respuesta:
```json
{"status": "queued", "job_id": "<celery-task-id>"}
```

---

## Tests

```powershell
pip install pytest
pytest -q tests/
```

---

## Estructura del proyecto

```
StackX/
├── docs/
│   ├── agents.md        # Definición de agentes consolidados
│   └── skills.md        # Contratos e interfaz de super-skills
├── backend/
│   └── app/
│       ├── main.py
│       ├── celery_app.py    # Celery application + Beat schedule
│       ├── tasks.py         # Celery tasks (sync_sanity)
│       ├── database.py
│       ├── models.py
│       ├── schemas.py
│       ├── recommender.py
│       ├── ai_client.py
│       ├── sanity_sync.py   # Core sync logic (no scheduler)
│       ├── skills_registry.py
│       └── ai_skills/
│           ├── content_generator.py
│           └── data_analysis.py
├── frontend/            # Next.js
├── tests/
└── docker-compose.yml
```

---

## Notas

- El endpoint `/admin/sync-groq/` solo requiere `ADMIN_TOKEN` si la variable está definida. En producción, proteger también a nivel de infraestructura (API Gateway, red privada).
- El proceso web (FastAPI) es completamente *stateless*: no ejecuta schedulers ni tareas periódicas in-process. Esto permite escalar réplicas sin duplicar jobs.
- El sync periódico lo gestiona **Celery Beat** usando `SYNC_INTERVAL_SECONDS` como intervalo configurado.
- Ver `BITACORA.md` para el registro completo de tareas completadas y pendientes.

[![Demo](https://img.shields.io/badge/Demo-Vercel-000000?style=flat-square&logo=vercel)](https://stackx-frontend.vercel.app)
[![CI](https://github.com/medalcode/StackX/actions/workflows/ci.yml/badge.svg)](https://github.com/medalcode/StackX/actions/workflows/ci.yml)

# StackX — Recomendador de Stack Tecnológico

Backend con FastAPI, SQLAlchemy y un motor de recomendación por pesos ponderados.
Incluye integración opcional con LLM (Ollama), Sanity/GROQ para gestión de contenido,
y un sistema de skills registrables para extender la lógica de recomendación.

---

## Arquitectura

La arquitectura sigue el principio de **agentes versátiles + super-skills paramétricas**.
Ver detalles en [`docs/agents.md`](docs/agents.md) y [`docs/skills.md`](docs/skills.md).

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

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r backend/requirements.txt
uvicorn backend.app.main:app --reload
```

El servidor levanta en `http://localhost:8000` con SQLite.

### Migraciones (Alembic)

```bash
cd backend
alembic upgrade head
```

Para generar una nueva migración tras cambiar modelos:

```bash
alembic revision --autogenerate -m "descripcion"
alembic upgrade head
```

### Sembrar datos de ejemplo

```bash
python -c "
from backend.app.database import SessionLocal
from backend.app.seed_data import seed
db = next(SessionLocal())
seed(db)
"
```

### Frontend (Next.js + Tailwind CSS)

```bash
cd frontend
npm install
npm run dev
```

### Docker Compose (todo junto)

```bash
docker-compose up --build
```

---

## Variables de entorno

| Variable | Default | Descripción |
|---|---|---|
| `DATABASE_URL` | `sqlite:///./dev.db` | URL de la base de datos |
| `OLLAMA_URL` | — | Endpoint del LLM (ej: `http://localhost:11434/v1/generate`) |
| `OLLAMA_TIMEOUT` | `10` | Timeout en segundos para llamadas al LLM |
| `JUSTIFICATION_SKILL` | — | Nombre de la skill a usar (`content_generator`, etc.) |
| `SANITY_PROJECT_ID` | — | ID del proyecto Sanity (activa sincronización) |
| `SANITY_DATASET` | `production` | Dataset de Sanity |
| `SANITY_API_VERSION` | `2024-01-01` | Versión de la API de Sanity |
| `SANITY_TOKEN` | — | Token de autenticación Sanity |
| `SYNC_INTERVAL_SECONDS` | `3600` | Frecuencia de sincronización periódica |
| `ADMIN_TOKEN` | — | Token para proteger el endpoint `/admin/sync-groq/` |
| `CORS_ORIGINS` | `*` | Orígenes permitidos (separados por coma) |

Copia `.env.example` a `.env` y configura los valores necesarios.

---

## Endpoints

### `GET /health`
Health check del servicio.

```bash
curl http://localhost:8000/health
```

### `POST /recommend-stack/`
Devuelve el top-3 de stacks recomendados según los pesos del usuario.

```bash
curl -X POST http://localhost:8000/recommend-stack/ \
  -H "Content-Type: application/json" \
  -d '{"weights": {"Escalabilidad": 0.9, "Facilidad": 0.5}, "proyecto": "Mi SaaS"}'
```

Header opcional `X-Justification-Skill: content_generator` para seleccionar skill explícita.

### `GET /recommend-stack/`
Versión paginada del mismo endpoint.

```bash
curl "http://localhost:8000/recommend-stack/?weights=%7B%22Escalabilidad%22%3A0.9%7D&skip=0&limit=5"
```

### `POST /admin/sync-groq/`
Dispara una sincronización desde Sanity/GROQ en background.

```bash
curl -X POST http://localhost:8000/admin/sync-groq/ \
  -H "Authorization: Bearer your_admin_token_here"
```

---

## Tests

```bash
pip install pytest
pytest -q tests/ -v
```

Actualmente **28 tests** en 6 suites:
- `test_api.py` — endpoints REST
- `test_models.py` — modelo de datos SQLAlchemy
- `test_recommender.py` — motor de recomendación
- `test_schemas.py` — schemas Pydantic
- `test_skill_contract.py` — skills y fallback LLM

### Lint

```bash
pip install ruff
ruff check backend/ tests/
ruff format --check backend/ tests/
```

---

## Estructura del proyecto

```
StackX/
├── backend/
│   ├── alembic/              # Migraciones (Alembic)
│   ├── alembic.ini
│   └── app/
│       ├── main.py
│       ├── database.py
│       ├── models.py
│       ├── schemas.py
│       ├── recommender.py
│       ├── ai_client.py
│       ├── sanity_sync.py
│       ├── skills_registry.py
│       ├── seed_data.py
│       ├── routes/
│       │   ├── recommend.py
│       │   └── admin.py
│       └── ai_skills/
│           ├── content_generator.py
│           └── data_analysis.py
├── frontend/                 # Next.js + Tailwind CSS
│   ├── pages/
│   ├── components/
│   ├── services/
│   ├── lib/
│   └── styles/
├── tests/                    # 28 tests
│   ├── conftest.py
│   ├── test_api.py
│   ├── test_models.py
│   ├── test_recommender.py
│   ├── test_schemas.py
│   └── test_skill_contract.py
├── docs/
├── docker-compose.yml
├── ANALISIS.md               # Reporte completo de mejoras
├── BITACORA.md               # Registro de desarrollo
└── AGENTS.md                 # Guía para agentes IA
```

---

## Stack técnico

| Capa | Tecnología |
|---|---|
| API | FastAPI (Python 3.11+) |
| Base de datos | SQLAlchemy 2.0 (SQLite / PostgreSQL) |
| Migraciones | Alembic |
| Frontend | Next.js 13 (Pages Router) + Tailwind CSS v4 |
| LLM | Ollama (opcional, vía httpx async) |
| CMS | Sanity/GROQ (opcional) |
| Scheduler | APScheduler (opcional) |
| CI | GitHub Actions (lint + test + build) |

---

## Mejoras recientes (v2.0)

- **28 tests** (vs 2 anteriores) con fixtures reutilizables
- **Alembic** para migraciones de base de datos
- **CORS** configurable
- **Skills asíncronas** (no bloquean el event loop)
- **Paginación** en endpoint de recomendaciones
- **Índices** en base de datos para performance
- **Logging** estructurado en todos los módulos
- **Frontend** migrado a Tailwind CSS v4 + TypeScript
- **ErrorBoundary** para manejo de errores en UI
- **Docker multi-stage** para frontend
- **Lint automático** con ruff en CI
- Ver `ANALISIS.md` para el reporte completo.

---

## Notas

- El endpoint `/admin/sync-groq/` solo requiere `ADMIN_TOKEN` si la variable está definida.
- El scheduler usa APScheduler en proceso. Para producción con múltiples réplicas, externalizar a Celery/RQ con Redis.
- Ver `BITACORA.md` para el registro completo de cambios.
- Ver `ANALISIS.md` para el análisis de debilidades y mejoras aplicadas.

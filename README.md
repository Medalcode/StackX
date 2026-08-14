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

### `POST /recommend-stack/export-markdown/`
Genera e imprime un dictamen técnico de arquitectura en formato Markdown estructurado.

```bash
curl -X POST http://localhost:8000/recommend-stack/export-markdown/ \
  -H "Content-Type: application/json" \
  -d '{"weights": {"Escalabilidad": 0.9}, "proyecto": "Mi SaaS"}'
```

### `POST /recommend-stack/favorites/` y `GET /recommend-stack/favorites/`
Guarda y consulta las configuraciones de stack favoritas seleccionadas por el usuario.

---

### Tests

```bash
pip install pytest pytest-asyncio pytest-cov
python -m pytest -v tests/

# Smoke tests (Ultra-rápido):
python -m pytest -m smoke
```

Actualmente **39 tests** en 8 suites (100% de éxito):
- `test_api.py` — endpoints REST (paginación, headers, rate limiting, exportador markdown, favoritos, admin tokens)
- `test_recommendation_service.py` — capa de servicio, caching SHA256 y exportador markdown
- `test_sanity_sync.py` — sincronización con Sanity y base de datos
- `test_models.py` — modelo de datos SQLAlchemy e índices
- `test_recommender.py` — motor de recomendación optimizado
- `test_schemas.py` — schemas Pydantic V2
- `test_skill_contract.py` — skills y fallback LLM en 3 niveles

### Lint

```bash
pip install ruff
python -m ruff check backend/ tests/
python -m ruff format --check backend/ tests/
```

---

## Estructura del proyecto

```
StackX/
├── backend/
│   ├── alembic/              # Migraciones (Alembic)
│   ├── alembic.ini
│   └── app/
│       ├── main.py           # FastAPI, Rate Limiting y Lifespan
│       ├── database.py
│       ├── models.py
│       ├── schemas.py
│       ├── recommender.py    # Motor de recomendación optimizado
│       ├── ai_client.py
│       ├── sanity_sync.py
│       ├── skills_registry.py
│       ├── seed_data.py
│       ├── services/         # Capa de Servicio (Service Layer + SHA256 Caching)
│       │   └── recommendation_service.py
│       ├── routes/
│       │   ├── recommend.py  # Endpoints REST (Recomendaciones, Export, Favoritos)
│       │   └── admin.py
│       └── ai_skills/
│           ├── content_generator.py
│           └── data_analysis.py
├── frontend/                 # Next.js + Tailwind CSS
│   ├── pages/
│   │   ├── index.jsx         # Formulario principal de sliders y recomendaciones
│   │   ├── compare.jsx       # Comparador Side-by-Side de arquitecturas
│   │   └── tech.jsx          # Catálogo de tecnologías (API REST)
│   ├── components/
│   ├── types/                # Interfaces TypeScript (index.ts)
│   ├── services/
│   ├── lib/
│   └── styles/
├── tests/                    # 39 tests (100% pasando)
│   ├── conftest.py
│   ├── test_api.py
│   ├── test_models.py
│   ├── test_recommendation_service.py
│   ├── test_recommender.py
│   ├── test_sanity_sync.py
│   ├── test_schemas.py
│   └── test_skill_contract.py
├── docs/
│   └── adr/                  # Architecture Decision Records (ADR-001, ADR-002, ADR-003)
├── docker-compose.yml
├── CHANGELOG.md              # Registro formal de versiones (Keep a Changelog)
├── ANALISIS.md               # Reporte completo de mejoras
├── BITACORA.md               # Registro de desarrollo
└── AGENTS.md                 # Guía para agentes IA
```

---

## Stack técnico

| Capa | Tecnología |
|---|---|
| API | FastAPI (Python 3.11+) + `slowapi` Rate Limiting |
| Base de datos | SQLAlchemy 2.0 (SQLite / PostgreSQL) |
| Migraciones | Alembic |
| Almacenamiento en Caché | `RecommendationCache` SHA256 in-memory (<1ms latencia) |
| Frontend | Next.js 13 (Pages Router) + Tailwind CSS v4 + TypeScript |
| LLM | Ollama (opcional, vía httpx async) |
| CMS | Sanity/GROQ (opcional) |
| Scheduler | APScheduler (controlado vía `ENABLE_IN_PROCESS_SCHEDULER`) |
| CI | GitHub Actions (lint + test + build) |

---

## Mejoras recientes (v2.0)

- **39 tests** (vs 2 anteriores) con fixtures reutilizables
- **Rate Limiting** integrado con `slowapi` contra ataques DoS
- **Almacenamiento en Caché SHA256** para respuestas <1ms en consultas repetitivas
- **Exportador de Reportes Ejecutivos** en Markdown estructurado
- **Comparador Side-by-Side** de arquitecturas en la UI (`/compare`)
- **Persistencia de Favoritos** (`/recommend-stack/favorites/`)
- **ADRs** (Architecture Decision Records) documentados en `docs/adr/`
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
- Ver `ANALISIS.md` y `CHANGELOG.md` para el reporte completo.

---

## Notas

- El endpoint `/admin/sync-groq/` solo requiere `ADMIN_TOKEN` si la variable está definida.
- El scheduler in-process está desactivado por defecto para entornos multi-worker y se habilita con `ENABLE_IN_PROCESS_SCHEDULER=true`.
- Ver `BITACORA.md` para el registro completo de cambios.
- Ver `ANALISIS.md` para el análisis de debilidades y mejoras aplicadas.


# StackX — Recomendador de Stack Tecnológico

Backend con FastAPI, SQLAlchemy y un motor de recomendación por pesos ponderados. Incluye integración opcional con LLM (Ollama) y Sanity/GROQ para gestión de contenido.

---

## Arquitectura

La arquitectura sigue el principio de **agentes versátiles + super-skills paramétricas**. Ver detalles en [`docs/agents.md`](docs/agents.md) y [`docs/skills.md`](docs/skills.md).

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
| `SANITY_TOKEN` | — | Token de autenticación Sanity |
| `SYNC_INTERVAL_SECONDS` | `3600` | Frecuencia de sincronización periódica |
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
Dispara una sincronización desde Sanity/GROQ en background.

```bash
curl -X POST http://localhost:8000/admin/sync-groq/ \
  -H "Authorization: Bearer your_admin_token_here"
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
│       ├── database.py
│       ├── models.py
│       ├── schemas.py
│       ├── recommender.py
│       ├── ai_client.py
│       ├── sanity_sync.py   # Incluye scheduler (fusionados)
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
- El scheduler usa APScheduler en proceso. Para producción con múltiples réplicas, externalizar a Celery/RQ con Redis como broker (ver `BITACORA.md`).
- Ver `BITACORA.md` para el registro completo de tareas completadas y pendientes.

# Skills — Convenciones e interfaz

## Resumen

Las "skills" son unidades reusables de lógica que realizan tareas relacionadas con la generación, transformación o enriquecimiento de datos (ej.: generación de justificaciones por LLM, enriquecimiento de metadatos, validaciones). Se ejecutan desde `ai_client` o desde workers/scheduler según el caso.

## Interfaz de una skill

Contrato mínimo recomendado:

- Nombre exportado: `SKILL_NAME` (string)
- Función entrypoint: `def run_skill(input: dict) -> dict` — devuelve un dict con al menos `status` y `result`.
- Metadatos opcionales: `TIMEOUT_SECONDS`, `DESCRIPTION`.

Ejemplo de `input` esperado:

```json
{
  "user_weights": {"backend": 1, "frontend": 0.5},
  "tech": {"id": 12, "name": "FastAPI", "attributes": {...}},
  "context": {"request_id": "..."}
}
```

Ejemplo de `output` esperado:

```json
{
  "status": "ok",
  "result": {
    "text": "Justificación...",
    "metadata": {"confidence": 0.87}
  }
}
```

## Registro y descubrimiento

Convención: colocar skills en `backend/app/ai_skills/` como módulos Python. Cada módulo exporta `SKILL_NAME` y `run_skill`.

Se recomienda implementar un registro central `backend/app/skills_registry.py` que:

- Explore `backend/app/ai_skills/` y cargue dinámicamente módulos.
- Exporte `get_skill(name) -> module` y `all_skills() -> List[str]`.

## Plantilla de skill (ejemplo)

```python
# backend/app/ai_skills/example_skill.py
SKILL_NAME = "example_justification"
TIMEOUT_SECONDS = 8
DESCRIPTION = "Skill de ejemplo que genera una justificación mínima."

def run_skill(input: dict) -> dict:
    tech = input.get("tech", {})
    tech_name = tech.get("name", "desconocido")
    text = f"Justificación básica para {tech_name}."
    return {"status": "ok", "result": {"text": text}}
```

## Super-Skills Paramétricas (Consolidación)

Para evitar la fragmentación, se prefieren "Super-Skills" que aceptan parámetros para variar su comportamiento.

### 1. `ContentGeneratorSkill`
**Propósito:** Sustituye a `JustificationSkill`, `TradeOffSkill` y `SummarySkill`.
**Parámetros clave:**
- `mode`: `"full_justification" | "concise_summary" | "technical_comparison"`.
- `target_audience`: `"cto" | "developer" | "product_owner"`.

### 2. `DataAnalysisSkill`
**Propósito:** Sustituye a `ScoringSkill`, `WeightCalculatorSkill` y `CompatibilitySkill`.
**Parámetros clave:**
- `operation`: `"calculate_stack_score" | "validate_compatibility" | "enrich_metadata"`.

## Registro de Skills Activas

Actualmente, las skills se han consolidado de la siguiente manera:
- `backend/app/ai_skills/content_generator.py` (Versátil)
- `backend/app/ai_skills/data_analysis.py` (Versátil)

---

## Timeouts, retries y manejo de errores

- Cada skill debe respetar `TIMEOUT_SECONDS` si está definido.
- Manejar excepciones y devolver `status: error` con `error` en el payload.
- Para llamadas externas usar retries con backoff y circuit-breaker donde aplique.

## Pruebas y contract tests

- Crear tests unitarios que importen la skill y validen que `run_skill` acepta el input mínimo y devuelve el schema esperado.
- Tests de contrato: mockear proveedor LLM y validar que la skill produce `result.text` con longitud mínima.

## Migración a ejecución asíncrona / workers

- Si la skill hace I/O pesado, convertirla a async o delegarla a un worker (Celery/RQ). Mantener la misma interfaz de entrada/salida en la cola (payload JSON).

## Checklist de despliegue

- Variables de entorno necesarias documentadas en `docs/agents.md`.
- Permisos para tokens (Sanity, LLM) correctamente configurados.
- Monitoreo (logs + métricas) habilitado para la skill.

"""Plantilla de skill: ejemplo mínimo.

Ruta: backend/app/ai_skills/example_skill.py
"""

SKILL_NAME = "example_justification"
TIMEOUT_SECONDS = 8
DESCRIPTION = "Skill de ejemplo que genera una justificación mínima."

def run_skill(input: dict) -> dict:
    """Genera una justificación simple basada en el nombre de la tecnología.

    Args:
        input: dict con keys opcionales `tech` y `user_weights`.

    Returns:
        dict con keys `status` y `result`.
    """
    try:
        tech = input.get("tech", {}) if isinstance(input, dict) else {}
        tech_name = tech.get("name", "desconocido")
        text = f"Justificación básica para {tech_name}."
        return {"status": "ok", "result": {"text": text}}
    except Exception as exc:
        return {"status": "error", "error": str(exc)}

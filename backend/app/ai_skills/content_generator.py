# backend/app/ai_skills/content_generator.py

SKILL_NAME = "content_generator"
DESCRIPTION = "Super-Skill para generar contenido variable (justificaciones, resúmenes, trade-offs) basado en parámetros."

def run_skill(input: dict) -> dict:
    mode = input.get("mode", "full_justification")
    tech = input.get("tech", {})
    tech_name = tech.get("name", "tecnología seleccionada")

    if mode == "full_justification":
        text = f"Justificación completa: {tech_name} es ideal por su escalabilidad y soporte de comunidad."
    elif mode == "concise_summary":
        text = f"Resumen: {tech_name} (Alta performance)."
    elif mode == "technical_comparison":
        text = f"Comparativa: {tech_name} frente a alternativas destaca por su baja latencia."
    else:
        text = f"Contenido generado para {tech_name} en modo {mode}."

    return {
        "status": "ok",
        "result": {
            "text": text,
            "mode_applied": mode
        }
    }

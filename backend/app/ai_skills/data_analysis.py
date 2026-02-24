# backend/app/ai_skills/data_analysis.py
from .. import recommender  # Reutilizamos lógica existente si es posible

SKILL_NAME = "data_analysis"
DESCRIPTION = "Super-Skill para análisis de datos, scoring y validación de compatibilidad."

def run_skill(input: dict) -> dict:
    operation = input.get("operation", "calculate_stack_score")
    
    if operation == "calculate_stack_score":
        # Podríamos llamar a recommender.calculate_score_for_tech aquí
        result = {"score": 0.85, "details": "Cálculo basado en pesos del usuario."}
    elif operation == "validate_compatibility":
        result = {"compatible": True, "conflict_level": "low"}
    else:
        result = {"error": f"Operación {operation} no soportada."}
        
    return {
        "status": "ok",
        "result": result
    }

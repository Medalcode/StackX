import os
import logging
import requests
from typing import Dict

logger = logging.getLogger("stackx.ai_client")
logger.setLevel(logging.INFO)

OLLAMA_URL = os.getenv("OLLAMA_URL")
OLLAMA_TIMEOUT = int(os.getenv("OLLAMA_TIMEOUT", "10"))

try:
    from .skills_registry import get_skill, all_skills, load_all_skills
    try:
        load_all_skills()
    except Exception:
        logger.warning("Failed to load skills on import", exc_info=True)
except Exception:
    logger.warning("Skills registry not available")
    def get_skill(name):
        return None

    def all_skills():
        return []


def _build_prompt(user_input: Dict, top_stack: Dict) -> str:
    proyecto = user_input.get("proyecto", "un proyecto")
    prioridades = user_input.get("weights", {})
    prompt = (
        f"Actúa como un Arquitecto Senior. El usuario quiere construir: {proyecto}. "
        f"Prioridades: {prioridades}.\n\n"
        f"El motor lógico ha determinado que el mejor stack es: {top_stack['name']}. "
        "Justifica en 3 puntos clave por qué este stack es el ideal para este caso específico, "
        "mencionando un trade-off que el usuario deba considerar. Responde en español técnico y claro."
    )
    return prompt


def _run_skill_if_available(user_input: Dict, top_stack: Dict, skill_name: str = None) -> str:
    """Intenta ejecutar una skill registrada para generar la justificación.

    Prioridad de selección de skill:
    1) `JUSTIFICATION_SKILL` env var
    2) primera skill registrada (si existe)
    Si falla o no existe, devuelve None para indicar que hay que usar LLM/fallback.
    """
    # precedence: explicit skill_name param > JUSTIFICATION_SKILL env var > first registered skill
    skill_name = skill_name or os.getenv("JUSTIFICATION_SKILL")
    try:
        if not skill_name:
            skills = all_skills()
            if skills:
                skill_name = skills[0]

        if not skill_name:
            return None

        module = get_skill(skill_name)
        if not module:
            return None

        payload = {
            "user_weights": user_input.get("weights", {}),
            "tech": top_stack,
            "context": {"request_id": user_input.get("request_id")}
        }
        result = module.run_skill(payload)
        if isinstance(result, dict) and result.get("status") == "ok":
            res = result.get("result") or {}
            if isinstance(res, dict):
                text = res.get("text")
                if text:
                    return text
            # if result.result is a string or fallback
            if isinstance(res, str) and res:
                return res
    except Exception:
        # No propagamos errores en la generación por skill; seguiremos al LLM/fallback.
        return None

    return None


def generate_justification(user_input: Dict, top_stack: Dict, skill_name: str = None) -> str:
    # 1) Intentar skill registrado (puede pasar un nombre de skill explícito)
    text = _run_skill_if_available(user_input, top_stack, skill_name=skill_name)
    if text:
        return text

    # 2) Intentar LLM externo
    prompt = _build_prompt(user_input, top_stack)

    if OLLAMA_URL:
        try:
            r = requests.post(OLLAMA_URL, json={"prompt": prompt}, timeout=OLLAMA_TIMEOUT)
            r.raise_for_status()
            data = r.json()
            # Expect provider to return {'text': '...'} or similar
            return data.get("text") or data.get("output") or str(data)
        except Exception:
            # fallback to local template
            pass

    # 3) Fallback determinista y seguro
    justification = (
        f"1) Rapidez de entrega: {top_stack['name']} permite iterar rápidamente y aprovechar ecosistemas maduros.\n"
        f"2) Ecosistema y librerías: ofrece amplia disponibilidad de paquetes y soporte.\n"
        f"3) Comunidad y contratación: fácil encontrar talento para mantener el producto.\n"
        f"Trade-off: Puede sacrificar rendimiento absoluto en tareas CPU-intensivas frente a alternativas más especializadas."
    )
    return justification

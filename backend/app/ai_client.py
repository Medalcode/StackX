import logging
import os

import httpx

logger = logging.getLogger("stackx.ai_client")

OLLAMA_URL = os.getenv("OLLAMA_URL")
OLLAMA_TIMEOUT = int(os.getenv("OLLAMA_TIMEOUT", "10"))

try:
    from .skills_registry import all_skills, get_skill, load_all_skills
    try:
        load_all_skills()
    except Exception as e:
        logger.warning("Failed to load skills on import: %s", e)
except Exception as e:
    logger.warning("Skills registry not available: %s", e)

    def get_skill(name):  # noqa: ARG001
        return None

    def all_skills():
        return []


def _build_prompt(user_input: dict, top_stack: dict) -> str:
    proyecto = user_input.get("proyecto", "un proyecto")
    prioridades = user_input.get("weights", {})
    prompt = (
        f"Actúa como un Arquitecto Senior. El usuario quiere construir: {proyecto}. "
        f"Prioridades: {prioridades}.\n\n"
        f"El motor lógico ha determinado que el mejor stack es: {top_stack['name']}. "
        "Justifica en 3 puntos clave por qué este stack es el ideal para este caso específico, "
        "un trade-off a considerar. Responde en español técnico y claro."
    )
    return prompt


async def _run_skill_if_available(user_input: dict, top_stack: dict, skill_name: str = None) -> str:
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
        result = await module.run_skill(payload)
        if isinstance(result, dict) and result.get("status") == "ok":
            res = result.get("result") or {}
            if isinstance(res, dict):
                text = res.get("text")
                if text:
                    return text
            if isinstance(res, str) and res:
                return res
    except Exception as e:
        logger.warning("Skill execution failed, falling back: %s", e)

    return None


async def generate_justification(user_input: dict, top_stack: dict, skill_name: str = None) -> str:
    text = await _run_skill_if_available(user_input, top_stack, skill_name=skill_name)
    if text:
        return text

    prompt = _build_prompt(user_input, top_stack)

    if OLLAMA_URL:
        try:
            async with httpx.AsyncClient() as client:
                r = await client.post(OLLAMA_URL, json={"prompt": prompt}, timeout=OLLAMA_TIMEOUT)
                r.raise_for_status()
                data = r.json()
                return data.get("text") or data.get("output") or str(data)
        except Exception as e:
            logger.error("Ollama call failed: %s", e)

    name = top_stack['name']
    justification = (
        f"1) Rapidez de entrega: {name} permite iterar rápidamente"
        " y aprovechar ecosistemas maduros.\n"
        f"2) Ecosistema y librerías: {name} ofrece amplia"
        " disponibilidad de paquetes y soporte.\n"
        f"3) Comunidad y contratación: fácil encontrar talento"
        " para mantener el producto.\n"
        "Trade-off: Puede sacrificar rendimiento absoluto en"
        " tareas CPU-intensivas frente a alternativas más"
        " especializadas."
    )
    return justification

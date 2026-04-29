"""Registro dinámico de skills.

Provee funciones para cargar módulos desde `backend/app/ai_skills/`, registrar y obtener skills.

API pública mínima:
- `load_all_skills()` -> None
- `get_skill(name)` -> module or None
- `all_skills()` -> List[str]
"""
import importlib.util
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SKILLS_FOLDER = ROOT / "ai_skills"

_registry: dict[str, object] = {}


def _load_module_from_path(path: Path):
    spec = importlib.util.spec_from_file_location(path.stem, str(path))
    if spec is None or spec.loader is None:
        raise ImportError(f"Cannot load spec for {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def load_all_skills():
    """Carga todos los módulos .py en `ai_skills` y registra aquellos que exportan `SKILL_NAME` y `run_skill`."""
    if not SKILLS_FOLDER.exists():
        return
    for p in SKILLS_FOLDER.glob("*.py"):
        if p.name.startswith("__"):
            continue
        try:
            module = _load_module_from_path(p)
            name = getattr(module, "SKILL_NAME", None)
            run = getattr(module, "run_skill", None)
            if name and callable(run):
                _registry[name] = module
        except Exception:
            # No propagamos errores en la carga automática; se recomienda loggear externamente.
            continue


def get_skill(name: str) -> object | None:
    return _registry.get(name)


def all_skills():
    return list(_registry.keys())


# Cargar al importar para conveniencia; la aplicación puede llamar explícitamente también.
try:
    load_all_skills()
except Exception:
    pass

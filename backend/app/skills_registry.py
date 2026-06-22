import importlib.util
import logging
import sys
from pathlib import Path

logger = logging.getLogger("stackx.skills_registry")

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
        except Exception as e:
            logger.warning("Failed to load skill %s: %s", p.name, e)


def get_skill(name: str) -> object | None:
    return _registry.get(name)


def all_skills():
    return list(_registry.keys())


try:
    load_all_skills()
except Exception as e:
    logger.error("Failed to load skills at import: %s", e)

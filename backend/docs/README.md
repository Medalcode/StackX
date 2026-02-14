# Documentación del backend

Este directorio contiene documentación y enlaces rápidos para desarrolladores del backend.

Documentación general y de diseño principal se encuentra en los MD globales:

- `../..`/docs/agent.md — especificación del agente y despliegue.
- `../..`/docs/skills.md — especificación de skills y plantillas.

Para integrar nuevas skills: crear módulos en `backend/app/ai_skills/` y, si es necesario, recargar `backend/app/skills_registry.py` o reiniciar la aplicación.

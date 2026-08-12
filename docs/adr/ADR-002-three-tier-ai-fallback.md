# ADR-002: Estrategia de Resiliencia en 3 Niveles para Justificaciones de IA

* **Estatus:** Aceptado
* **Fecha:** 2026-08-12
* **Autor:** Staff Software Architect

## Contexto
El motor de recomendaciones de StackX genera explicaciones en lenguaje natural mediante IA. Depender de un único proveedor de LLM local o externo puede provocar caídas completas del servicio en caso de problemas de red o indisponibilidad del modelo.

## Decisión
Implementar un patrón de degradación elegante (*Fallback Chain*) de tres niveles en [`ai_client.py`](file:///c:/Users/Jonatthan/Documents/Github/StackX/backend/app/ai_client.py):
1. **Nivel 1 (Super-Skills Registry):** Ejecutar la habilidad de IA seleccionada (`content_generator`).
2. **Nivel 2 (Ollama HTTP Client):** Invocar el servidor LLM vía HTTP asíncrono si está disponible.
3. **Nivel 3 (Plantilla Estática Determinista):** Generar una justificación basada en plantillas deterministas precalculadas si los niveles anteriores fallan.

## Consecuencias
* **Positivas:**
  - Tolerancia a fallos total: la aplicación responde al usuario en el 100% de los casos.
  - Cero dependencias duras con servicios externos fuera de línea.
* **Negativas:**
  - La respuesta de Nivel 3 es estática y no posee la creatividad dinámica de un modelo LLM activo.

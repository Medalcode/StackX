# ADR-003: Almacenamiento en Caché SHA256 y Protección por Rate Limiting

* **Estatus:** Aceptado
* **Fecha:** 2026-08-12
* **Autor:** Staff Software Architect

## Contexto
El cálculo repetido de recomendaciones y la generación asíncrona de justificaciones mediante habilidades de IA imponía una carga innecesaria en la base de datos y en los clientes LLM. Adicionalmente, los endpoints de la API pública requerían protección contra abuso o denegación de servicio (DoS).

## Decisión
1. **Rate Limiting Middleware:** Integrar `slowapi` en la aplicación FastAPI para limitar peticiones excesivas (por defecto 60/minuto global y 30/minuto por endpoint sensible).
2. **Capa de Almacenamiento en Caché:** Implementar `RecommendationCache` en [`recommendation_service.py`](file:///c:/Users/Jonatthan/Documents/Github/StackX/backend/app/services/recommendation_service.py) almacenando hashes `SHA256` de los parámetros de consulta con TTL determinista.

## Consecuencias
* **Positivas:**
  - Reducción drástica de la latencia para consultas repetitivas de **~2000ms a < 1ms**.
  - Protección de resiliencia ante ataques de denegación de servicio (DoS).
* **Negativas:**
  - Las respuestas en caché no reflejan inmediatamente cambios en la base de datos hasta que transcurra el TTL (300 segundos) o se vacíe la caché.

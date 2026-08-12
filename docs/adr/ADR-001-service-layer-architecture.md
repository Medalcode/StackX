# ADR-001: Adopción de Capa de Servicio (Service Layer)

* **Estatus:** Aceptado
* **Fecha:** 2026-08-12
* **Autor:** Staff Software Architect

## Contexto
Los controladores de la API REST (`backend/app/routes/recommend.py`) acoplaban la consulta de base de datos, el cálculo de scoring relacional, la invocación asíncrona de IA y la respuesta HTTP. Esto violaba el principio de responsabilidad única (SRP) y duplicaba la orquestación entre endpoints POST y GET.

## Decisión
Extraer la lógica de orquestación a una capa de servicios desacoplada [`recommendation_service.py`](file:///c:/Users/Jonatthan/Documents/Github/StackX/backend/app/services/recommendation_service.py). Los controladores HTTP actúan únicamente como delegados del servicio.

## Consecuencias
* **Positivas:**
  - Controladores HTTP limpios, desacoplados y fácilmente testeables.
  - Reutilización DRY de la orquestación asíncrona de IA entre peticiones POST y GET.
  - Facilidad para incorporar almacenamiento en caché (Redis) sin alterar las rutas HTTP.
* **Negativas:**
  - Adición de un archivo de módulo adicional en la arquitectura.

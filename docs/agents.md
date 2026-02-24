# Arquitectura de Agentes — StackX

## Agente Generalista: `ArchitectAgent`
**Rol:** Arquitecto de Soluciones Senior.
**Responsabilidad:** Orquestar el flujo completo desde la recepción de requerimientos del usuario hasta la entrega de un stack recomendado con su respectiva justificación.
**Capacidades:**
- Consultar el motor de recomendación (Skill: `AnalysisSkill`).
- Generar explicaciones técnicas y de negocio (Skill: `ContentGeneratorSkill`).
- Resolver conflictos entre prioridades (Costo vs Performance).

## Agente de Integración: `DataAgent`
**Rol:** Curador de Datos e Integración.
**Responsabilidad:** Garantizar que la base de conocimientos tecnológica esté sincronizada y limpia.
**Capacidades:**
- Sincronización con Sanity/GROQ.
- Auditoría de metadatos de tecnologías.
- Actualización de compatibilidades.

---
*Nota: Se han fusionado los antiguos 'RecommendationAgent' y 'JustificationAgent' en el 'ArchitectAgent' para reducir la sobrecarga de cambio de contexto y la redundancia en prompts.*

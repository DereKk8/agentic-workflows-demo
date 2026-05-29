# Sistema Agéntico de Mesa de Ayuda Académica

Prototipo académico con FastAPI + PostgreSQL que demuestra un flujo agéntico sobre tickets de soporte: clasificación, búsqueda de conocimiento, redacción y supervisión.

## Requisitos

- Docker y Docker Compose
- (Opcional modo real) API key de Groq, OpenRouter o Gemini

## Ejecución rápida

```bash
docker compose up --build
```

- API y dashboard: `http://localhost:8000`
- Health check: `GET /api/health`

Detener:

```bash
docker compose down
```

## Variables de entorno

- `MODO_AGENTE`: `mock` (default) o `real`
- `PROVEEDOR_LLM`: `groq` (default), `openrouter`, `gemini`
- `GROQ_API_KEY`
- `OPENROUTER_API_KEY`
- `GEMINI_API_KEY`

## Endpoints principales

- `GET /api/health`
- `POST /api/seed`
- CRUD tickets:
  - `GET /api/tickets`
  - `POST /api/tickets`
  - `PUT /api/tickets/{ticket_id}`
  - `DELETE /api/tickets/{ticket_id}`
- CRUD artículos:
  - `GET /api/articulos`
  - `POST /api/articulos`
  - `PUT /api/articulos/{articulo_id}`
  - `DELETE /api/articulos/{articulo_id}`
- Workflow:
  - `POST /api/workflow/ejecutar/{ticket_id}`
- Trazas:
  - `GET /api/tickets/{ticket_id}/ejecuciones`

## Validación manual (oficial)

1. `GET /api/health` devuelve estado `ok`.
2. `GET /api/tickets` y `GET /api/articulos` muestran datos seed.
3. Ejecutar CRUD completo de tickets (crear, listar, editar, eliminar).
4. Ejecutar CRUD completo de artículos (crear, listar, editar, eliminar).
5. Ejecutar `POST /api/workflow/ejecutar/{ticket_id}` en modo `mock`.
6. Verificar campos de salida: clasificación, artículos usados, respuesta, escalamiento y pasos.
7. Verificar persistencia de traza en `GET /api/tickets/{ticket_id}/ejecuciones`.
8. (Opcional) Cambiar a modo `real` con proveedor y API key válida; repetir ejecución.

## Notas de diseño

- Modo `mock` es determinista y suficiente para la demostración.
- Modo `real` usa CrewAI (semántica de agentes/tareas) y LangChain (invocación de proveedor).
- Las tablas se crean automáticamente en startup.
- No se implementan autenticación, colas, workers, ni frontend separado.


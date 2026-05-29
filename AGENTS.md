# Repository Guidelines

## Project Structure & Module Organization

Current planning artifacts:

- `prd.md`: implementation decisions for the Agentic Academic Help Desk prototype.
- `plan-proyecto-agentica.md`: original academic project plan; keep unchanged unless explicitly requested.

When implementation begins, keep this PRD-aligned structure:

- `app/`: FastAPI backend, domain models, routes, workflow, and dashboard serving.
- `app/static/`: plain HTML, CSS, and JavaScript dashboard.
- `docs/`: Mermaid diagrams and Spanish academic documentation.
- `postman/`: exported Postman collection for API validation.
- `docker-compose.yml` and `Dockerfile`: local API and PostgreSQL deployment.

## Build, Test, and Development Commands

No runnable application files are present yet. Once added, use:

- `docker compose up --build`: build and run FastAPI with PostgreSQL.
- `docker compose down`: stop local containers.
- `python -m uvicorn app.main:app --reload`: run the API outside Docker.
- `pytest`: run automated tests if a test suite is later introduced.

Document any required setup, validation, or demo command in `README.md`.

## Coding Style & Naming Conventions

Use Python for the backend. Keep modules focused by responsibility: routes, schemas, persistence, workflow, and provider integrations. Use `snake_case` for files, functions, and variables; use `PascalCase` for classes and ORM models.

Use Spanish domain names at the API, schema, and domain level, such as `Ticket`, `ArticuloConocimiento`, and `EjecucionAgente`. Infrastructure code may use conventional English names when clearer.

Keep labels, README content, Postman descriptions, diagrams, and presentation-facing text in Spanish.

## Testing Guidelines

The MVP does not require automated tests. Postman is the official validation artifact. Cover health checks, seed data, ticket CRUD, knowledge article CRUD, mock agent execution, optional real execution, and trace retrieval.

Mock mode must be sufficient for normal validation. Test real LLM mode only when credentials are available.

## Commit & Pull Request Guidelines

This directory is not currently a Git repository, so no local commit history is available. After Git is initialized, use clear imperative commits, for example: `add ticket CRUD endpoints`.

Pull requests should include a summary, validation steps, linked issue or task context, and screenshots for dashboard changes. Do not commit API keys, local video scripts, `.env` files, or private credentials.

## Security & Configuration Tips

Default to deterministic mock mode. Keep provider keys in environment variables, for example `GROQ_API_KEY`. Document optional OpenRouter or Gemini setup without requiring it for the demo.

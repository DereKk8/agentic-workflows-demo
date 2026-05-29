# PRD: Agentic Academic Help Desk Prototype

## Problem Statement

The project needs a focused, academically defensible prototype that demonstrates agentic AI workflows without becoming a large production system. The prototype must satisfy the project requirements for CRUD operations, Docker-based deployment, Postman API validation, academic documentation, and the use of current agentic AI ecosystem tools, specifically LangChain and CrewAI.

The main risk is overengineering: a full help desk platform with authentication, complex roles, realtime messaging, background workers, advanced search, or a heavy frontend would consume time without improving the academic objective. The project needs a small but polished system that makes the agent workflow visible, explainable, and easy to demonstrate.

## Solution

Build a small educational prototype called an **Agentic Academic Help Desk System**. The system will let a user create academic support tickets and knowledge base articles, then execute an agentic workflow over a selected ticket.

The workflow will classify the ticket, search relevant knowledge articles, draft a suggested response, and decide whether the ticket should be escalated. The system will run in deterministic mock mode by default, with an optional real LLM mode using Groq as the default provider. OpenRouter and Google Gemini will be documented as alternative providers.

The application will be implemented as a single FastAPI backend with a lightweight, polished, single-page dashboard served by the backend. PostgreSQL will run through Docker Compose. The dashboard will visualize the agentic execution as a step-by-step workflow, while the API and Postman collection will provide the required CRUD and validation surface.

All final user-facing project artifacts should be in Spanish, except this PRD, which is intentionally written in English.

## User Stories

1. As a professor, I want to see a small but complete prototype, so that I can evaluate the agentic architecture without unnecessary implementation noise.
2. As a student developer, I want a limited implementation scope, so that the project can be completed reliably within the available time.
3. As a demo user, I want to create academic support tickets, so that I can simulate real requests from students or teachers.
4. As a demo user, I want to view a list of tickets, so that I can choose which case to analyze.
5. As a demo user, I want to edit a ticket, so that I can correct or refine the support request before executing the agent workflow.
6. As a demo user, I want to delete sample tickets, so that I can reset or clean demo data.
7. As a demo user, I want to create knowledge base articles, so that the agents have institutional information to use.
8. As a demo user, I want to view knowledge base articles, so that I can understand what information the system may use during analysis.
9. As a demo user, I want to edit knowledge base articles, so that the demonstration can cover different academic scenarios.
10. As a demo user, I want to delete knowledge base articles, so that I can keep the sample knowledge base small and relevant.
11. As a demo user, I want to run the full agent workflow from a single button, so that the system feels like one coherent use case instead of disconnected demo functions.
12. As a demo user, I want the workflow to show classification, knowledge search, response drafting, and supervision steps, so that I can understand how the agents collaborate.
13. As a demo user, I want the dashboard to animate the workflow while the backend request runs, so that the agentic process is easy to present visually.
14. As a demo user, I want to see the final suggested response, so that I can evaluate the practical output of the workflow.
15. As a demo user, I want to see whether the ticket requires escalation, so that the human-in-the-loop decision is clear.
16. As a demo user, I want to see which knowledge articles were used, so that the generated response is traceable.
17. As a demo user, I want to review past agent executions for a ticket, so that I can compare multiple runs.
18. As a demo user, I want mock mode to work without an API key, so that the project can always be demonstrated.
19. As a demo user, I want a real AI mode toggle, so that the project can demonstrate actual LLM inference when credentials are available.
20. As a student developer, I want Groq to be the default real inference provider, so that real mode is fast and free-plan friendly.
21. As a student developer, I want OpenRouter and Gemini documented as alternatives, so that the project is not tied to one provider.
22. As a student developer, I want classification to be deterministic, so that the demo remains predictable.
23. As a student developer, I want knowledge search to be deterministic, so that article retrieval is explainable.
24. As a student developer, I want LLM inference limited to response drafting and supervision, so that API cost and runtime fragility stay low.
25. As a student developer, I want CrewAI included in the agent implementation, so that the project satisfies the required technology scope.
26. As a student developer, I want LangChain included in the LLM provider abstraction, so that model invocation is explicit and swappable.
27. As a student developer, I want the application to create database tables automatically on startup, so that no migration workflow is needed.
28. As a student developer, I want Docker Compose to start both the API and database, so that setup is reproducible.
29. As a student developer, I want seed demo data, so that the project can be demonstrated immediately after startup.
30. As a student developer, I want a Postman collection, so that the required API validation artifact is available.
31. As a student developer, I want a manual validation plan, so that the project can be tested without an automated test suite.
32. As a reader of the academic report, I want the prototype architecture to map cleanly to C4 and UML-style diagrams, so that the implementation supports the written analysis.
33. As a reader of the academic report, I want trace records for agent executions, so that observability and auditability can be discussed concretely.
34. As a presentation viewer, I want a polished visual dashboard, so that the agentic workflow is easier to understand than raw API calls.
35. As a future maintainer, I want the system to avoid authentication, background workers, queues, and frontend build tooling, so that the prototype remains easy to understand.

## Implementation Decisions

- The domain will be an academic help desk where support tickets are resolved with assistance from an agentic workflow.
- The project name for user-facing Spanish artifacts should be based on "Sistema Agéntico de Mesa de Ayuda Académica".
- The application will be a single FastAPI service.
- The same FastAPI service will expose the API and serve the static dashboard.
- The dashboard will be lightweight static HTML, CSS, and JavaScript, without React, Vue, Next.js, or a separate frontend build pipeline.
- PostgreSQL will be used as the runtime database through Docker Compose.
- The application will automatically create tables on startup.
- No migration system will be introduced for the MVP.
- The API container and PostgreSQL container will be the only required runtime services.
- The core domain entities will be `Ticket`, `ArticuloConocimiento`, and `EjecucionAgente`.
- `Ticket` will support full CRUD operations.
- `ArticuloConocimiento` will support full CRUD operations.
- `EjecucionAgente` will be created by the system as an execution trace and exposed as read-only data.
- No separate `Usuario` entity will be implemented.
- No separate `Curso` entity will be implemented; course information can be represented as a simple field.
- No authentication or authorization will be implemented.
- The public workflow boundary will be one endpoint that executes the complete agent workflow for a ticket.
- The API will not expose separate public endpoints for each internal agent step.
- The agent workflow will be synchronous from the backend perspective.
- The dashboard may animate progress while waiting for the synchronous backend response.
- No WebSockets, polling loops, queues, or background workers will be added.
- The workflow will contain four conceptual agents: classifier, knowledge searcher, response writer, and supervisor.
- The classifier agent will use deterministic rules.
- The knowledge search agent will use deterministic database search and simple scoring.
- The response writer agent will use deterministic templates in mock mode and LLM inference in real mode.
- The supervisor agent will use deterministic rules in mock mode and LLM inference in real mode.
- Mock mode will be the default mode.
- Real inference mode will be optional and require provider credentials.
- Groq will be the default real inference provider.
- OpenRouter and Google Gemini will be documented as alternative providers.
- If real mode is selected without valid credentials, the system should fail gracefully or fall back with a clear Spanish message.
- CrewAI will be used to express agent and task semantics in the real-inference path.
- LangChain will be used to abstract LLM/provider invocation where practical.
- The implementation will use Spanish domain names at the API/schema/domain level.
- The implementation may use conventional English names for infrastructure modules and framework-oriented code.
- The API, dashboard labels, README, Postman collection descriptions, diagrams, LaTeX document, and presentation material should be in Spanish.
- This PRD is the exception and remains in English.
- Mermaid source files will be used for architecture and workflow diagrams.
- The documentation set will include a Spanish README, Mermaid diagrams, a Spanish LaTeX report, a Postman collection, and Spanish presentation support material.
- The explanatory video script should remain local-only and should not be part of the public repository.

## Testing Decisions

- The project will not include an automated unit or integration test suite for the MVP.
- Postman will be the official API validation artifact.
- The README will include a Spanish manual validation plan.
- The Postman collection should cover health check, seed data, ticket CRUD, knowledge article CRUD, mock agent execution, optional real agent execution, and execution trace retrieval.
- Manual validation should focus on externally visible behavior: API responses, persisted data, dashboard behavior, and trace output.
- Manual validation should not depend on private implementation details.
- Real LLM calls should not be required for validation.
- Mock mode must be sufficient to demonstrate the complete workflow.
- Real mode should be validated manually only when an API key is available.

## Out of Scope

- User authentication and authorization.
- User management.
- Role-based access control.
- Full help desk administration workflows.
- Realtime chat.
- Email notifications.
- File attachments.
- Background jobs or queues.
- WebSockets or server-sent events.
- Vector databases.
- Embedding pipelines.
- Advanced semantic search.
- Production observability tooling.
- CI/CD setup.
- Automated unit tests.
- Automated integration tests.
- Browser automation tests.
- A separate frontend application.
- Mobile application support.
- Multi-tenant architecture.
- Complex deployment beyond local Docker Compose.
- Payment, legal, medical, or financial advice domains.

## Further Notes

The project should stay intentionally small. The value of the prototype comes from showing a clear agentic workflow over concrete CRUD entities, not from building a complete production help desk system.

The dashboard is important because it makes the agentic workflow visible during the presentation. The UI should be polished enough to demonstrate the project professionally, but it should remain narrow: ticket selection, mode/provider controls, workflow visualization, final response, escalation decision, and execution history.

The academic documentation should use the implementation as evidence for architectural analysis. The trace entity is especially useful for discussing observability, maintainability, auditability, human-in-the-loop supervision, and quality attributes.

The original Spanish project plan file must remain unchanged. This PRD is a separate implementation planning artifact derived from the design decisions made during the conversation.

# eudai - Technical Design (Spec-Driven Workflow)

## Architecture Overview

```txt
+--------------------+  WebSocket/REST   +-----------+  HTTP API  +------------+
|     Client       | <---------------->| Server   | <------------> | Ollama     |
| (Webapp + TUI/CLI) |                   | (FastAPI) |                | (DeepSeek) |
+--------------------+                   +-----------+                +------------+
     |                                         |
     |   CLI/TUI (Commander/Chalk)             | (WS: chat, REST: files, project mgmt)
     |-----------------------\                 |
                             \                 v
                        +-----------------------------+
                        |        PostgreSQL           |
                        +-----------------------------+
```

- **Client**: The combined user interface layer, containing both the **Web App** (`client/webapp`, React) and the **CLI/TUI** (`client/cli`, Commander/Chalk). Both are TypeScript, managed as a monorepo (pnpm).
- **Server**: FastAPI (Python 3.15), managed with **uv** for dependencies/environment, async with PostgreSQL (asyncpg/SQLAlchemy), Alembic for migrations.
- **LLM**: Ollama (container, DeepSeek model), HTTP API.
- **Data Persistence**: PostgreSQL (docker volume).

---

## Data Flows

- **WebSocket**: Client (webapp/TUI) <-> Server
  - Real-time chat (send/receive), streaming LLM responses.
  - Project/conversation/file updates if needed.
- **REST**: Client (webapp/TUI) <-> Server
  - CRUD for users, projects, files, URLs, instructions.
  - Auth, file upload/download, initial data bootstrapping.
- **Ollama API**: Server <-> Ollama
  - HTTP, async, streaming LLM responses.
- **DB**: Server <-> PostgreSQL
  - All data persistence.

---

## API Contracts

### WebSocket (for real-time chat)

- **Connect**: `/ws/chat`
- **Protocol**: JSON messages, event-based.

**Sample Payloads:**

```json
// Client -> Server
{ "type": "chat_prompt", "project_id": "proj-123", "conversation_id": "conv-456", "text": "What is eudaimonia?" }
{ "type": "file_upload_init", "project_id": "proj-123", "filename": "doc.pdf" }

// Server -> Client
{ "type": "chat_response", "conversation_id": "conv-456", "stream": true, "text": "Eudaimonia is..." }
{ "type": "file_upload_progress", "file_id": "file-789", "progress": 0.4 }
{ "type": "error", "message": "Invalid project ID" }
```

### REST Endpoints (Draft)

| Method | Path                        | Description                          |
|--------|-----------------------------|--------------------------------------|
| POST   | `/api/auth/login`           | Login, returns JWT                   |
| POST   | `/api/auth/signup`          | Create user                          |
| GET    | `/api/projects`             | List projects                        |
| POST   | `/api/projects`             | Create project                       |
| GET    | `/api/projects/:id`         | Get project details                  |
| PUT    | `/api/projects/:id`         | Update project                       |
| DELETE | `/api/projects/:id`         | Delete project                       |
| GET    | `/api/projects/:id/files`   | List files in project                |
| POST   | `/api/projects/:id/files`   | Upload file (multipart)              |
| GET    | `/api/files/:file_id`       | Download file                        |
| GET    | `/api/conversations/:id`    | Get conversation messages            |
| GET    | `/api/health`               | Health check                         |

---

## Database Schema (Draft)

- **users**
  - id (uuid, pk)
  - username (unique)
  - email (unique)
  - password_hash
  - created_at
- **projects**
  - id (uuid, pk)
  - owner_id (fk -> users)
  - name
  - description
  - created_at
- **conversations**
  - id (uuid, pk)
  - project_id (fk -> projects)
  - title
  - created_at
- **messages**
  - id (uuid, pk)
  - conversation_id (fk -> conversations)
  - sender ("user"|"llm")
  - text
  - timestamp
- **files**
  - id (uuid, pk)
  - project_id (fk -> projects)
  - filename
  - path
  - uploaded_at
  - uploaded_by (fk -> users)
- **instructions**
  - id (uuid, pk)
  - project_id (fk -> projects)
  - instruction_text
  - created_at
- **urls**
  - id (uuid, pk)
  - project_id (fk -> projects)
  - url
  - description
  - added_by (fk -> users)
  - created_at

---

## Authentication

- JWT (via FastAPI dependency)
- Secure cookies for web, bearer for API/CLI
- Permissions: project ownership, file access

---

## Error Handling

| Error Type        | Source      | Procedure                  | API Response          | Log? |
|-------------------|-------------|----------------------------|-----------------------|------|
| Ollama Unreachable| Backend     | Retry x3, fail gracefully  | 503 LLM unavailable   | Yes  |
| Postgres Down     | Backend     | Fail fast                  | 503 Storage error     | Yes  |
| File Upload Error | Backend     | Validate, return error     | 400 Bad file          | Yes  |
| Auth Failure      | Backend     | Return error               | 401 Unauthorized      | Yes  |
| Invalid Data      | Backend     | Validate, return error     | 400 Bad request       | Yes  |

---

## Deployment

- All components run as Docker containers (multi-stage, minimal images).
- **Backend**: Python 3.15, FastAPI, dependencies managed and run via **uv**.
- **LLM**: Ollama container, DeepSeek R1 model.
- **DB**: PostgreSQL container, volume for persistence.
- Compose healthchecks and wait scripts for dependencies.
- Volumes for persistence (`db`, `ollama-models`, file uploads).
- Non-root user in all containers.

---

## Testing

- **Server:** pytest, httpx for API, WebSocket test client, coverage.
- **Client:** Vitest, Cypress/Playwright, Storybook for UI.

---

## CI/CD

- GitHub Actions: lint, test, build, image scan.
- Commitizen (cz-emoji-conventional) for semantic/emoji changelog.

---

## Directory Structure

```plaintext
eudai/
  client/
    webapp/    # React app (web)
    cli/       # Commander/Chalk TUI/CLI
    Dockerfile.client   # Multi-stage, Bun+TS+React+UnoCSS
    package.json
    pnpm-workspace.yaml
  server/     # FastAPI Python Server (uv)
    Dockerfile.server   # Multi-stage, FastAPI+uv (NO PDM)
    Dockerfile.gpu      # For GPU Ollama (if needed)
  docs/
    requirements.md      # EARS Notation
    design.md            # Technical design (this file)
    tasks.md             # Implementation plan
    adr/                 # Architecture decision records
  docker-compose.yml     # Orchestration
  docker-compose.gpu.yml # GPU override
  README.md
```

---

## Summary of Key Architecture Decisions

- **Client** includes both webapp and CLI/TUI, with shared code and configuration.
- **Server** is Python (FastAPI, managed by uv), with WebSocket and REST APIs.
- **Ollama** is integrated as a service for DeepSeek LLM, accessible via HTTP from Server.
- **Data persistence** is via PostgreSQL, with Alembic for migrations.
- **Multi-stage Docker builds** and docker-compose orchestration for security and performance.
- **Testing and CI/CD** is first-class, using Vitest, Playwright/Cypress, Pytest, and GitHub Actions.

---
<!-- ADR_START -->
## Architecture Decision Records (ADRs)

- [Ollama as distinct service](2025/08/2025-08-06-ollama-as-distinct-service.md)
- [Docker Compose vs Kubernetes](2025/08/2025-08-09_docker-compose-vs-kubernetes.md)
- [index](index.md)
<!-- ADR_END -->

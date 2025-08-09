# eudai - Technical Design (Spec-Driven Workflow)

## Architecture Overview

```txt
+--------------------+  WebSocket/REST   +-----------+  HTTP API  +------------+
|     Client       | <---------------->| Server   | <------------> | Ollama     |
| (Webapp + TUI/CLI) |                   | (FastAPI) |                | (DeepSeek) |
+--------------------+                   +-----------+                +------------+
     |                                         |
     |   CLI/TUI (Commander/Chalk)             | (WS/REST: chat, files, project mgmt)
     |-----------------------\                 |
                             \                 v
                        +-----------------------------+
                        |        PostgreSQL           |
                        +-----------------------------+
```

- **Client**: The combined user interface layer, containing both the **Web App** (`Client/webapp`, React) and the **CLI/TUI** (`Client/cli`, Commander/Chalk). Both are TypeScript, use Bun+pnpm, and share a monorepo structure.
- **Server**: FastAPI (Python 3.15), managed with PDM, async with PostgreSQL (asyncpg/SQLAlchemy), Alembic for migrations.
- **LLM**: Ollama (container, DeepSeek model), HTTP API.
- **Data Persistence**: PostgreSQL (docker volume).

---

## Data Flows

- **WebSocket**: Client (webapp/TUI) <-> Server
  - Real-time chat (send/receive), streaming LLM responses.
  - Project/conversation/file updates.

- **REST**: Client (webapp/TUI) <-> Server
  - CRUD for users, projects, conversations, files, URLs.
  - Auth, file upload/download, initial data bootstrapping.

- **Ollama API**: Server <-> Ollama
  - HTTP, async, streaming LLM responses.

- **DB**: Server <-> PostgreSQL
  - All data persistence.

---

## API Contracts

### WebSocket

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

<!-- markdownlint-disable MD007 -->
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

- All errors returned in `{ "type": "error", "message": "..." }` via WebSocket or as JSON via REST.
- Healthcheck endpoint `/api/health` for orchestration (docker-compose).

---

## Deployment

- All components run as Docker containers (multi-stage, minimal images).
- CPU/GPU Ollama support via compose override.
- Server waits for DB/Ollama (healthcheck/wait scripts).
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
  server/     # FastAPI Python Server (PDM)
    Dockerfile.server   # Multi-stage, FastAPI+PDM
    Dockerfile.gpu      # For GPU Ollama
  docs/
    requirements.md      # EARS Notation
    design.md            # Technical design (this file)
    backlog.md           # Implementation plan
    adr/                 # Architecture decision records
  docker-compose.yml     # Orchestration
  docker-compose.gpu.yml # GPU override
  README.md
```

---

## Error Matrix

| Scenario                   | Expected Result             | Fallback/Error                |
|----------------------------|----------------------------|-------------------------------|
| File upload > limit        | Reject, inform user         | 413 error                     |
| Ollama not ready           | Error page/message          | Log + retry/backoff           |
| DB connection loss         | Serve error/maintenance     | Log + retry/backoff           |
| Model download slow        | Progress log, graceful wait | User notification             |
| Disk full                  | Error on upload             | Log + maintenance alert       |
| TUI in non-TTY             | Fallback to plain text      | Exit with message             |

---

## Summary of Key Architecture Decisions

- **Client** includes both webapp and CLI/TUI, with shared code and configuration.
- **Server** is Python (FastAPI, PDM managed), with WebSocket and REST APIs.
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

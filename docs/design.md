# eudai - Technical Design (Spec-Driven Workflow)

## Architecture Overview - MVP (v 1.0.0)

+--------------------+   WebSocket  +-----+   WS + REST API   +------------------+
|     Client         | <----------> |  Server   | <---------> | AI Model         |
| (Terminals/CLIs)   |              | (FastAPI) |             | (deepseek)       |
|   TypeScript       |              |  Python   |             | Docker container |
+--------------------+              +-----------+             +------------------+
     |                               |
     |                               | (Stores chat history,contexts,etc)
     |------------------\            |
                         \           v
              +------------------------+
              |   PostgreSQL Database  |
              +------------------------+

- **Client**: The user interface layer located in the `client` directory. Written using `ESM` (versus `CJS` -- aka `esmodules` versus `commonjs`) and the `TypeScript` superset of `JavaScript`, the package is managed with `pnpm`.
- **Server**: `FastAPI` (`Python 3.13`), dependencies/environment are managed with **`uv`**, async data flowing to a `PostgreSQL` database (`asyncpg`/`SQLAlchemy`), and uses `Alembic` for migrations.
- **LLM**: `deepseek` model via `Ollama` and `docker-compose`andHTTP API.
- **Data Persistence**: `PostgreSQL` (using a Docker volume via `docker-compose`).

## Data Flows

- **WebSocket API (primary for chat/streaming)**: Client <-> Server
  - WebSockets are the primary vehicle for real-time data flow.
  - HTTP will be the fallback for real-time data flow in case there is an issue with the WebSocket API.
  - Real-time chat (send/receive) and streaming LLM responses.
  - Project/conversation/file updates if needed.
- **HTTP/REST API (fallback + async operations)**: Client <-> Server
  - CRUD for users, projects, files, URLs, instructions.
  - Auth, file upload/download, initial data bootstrapping.
- **Database Persistence layer**: Server <-> `PostgreSQL`
  - All data persistence.
- **Config Management**: `python-dotenv`
  - A `.env` file stores DB connection strings, model settings, etc.
  - `python-dotenv` automatically loads this at FastAPI startup
  - Actual env vars can still be overridden, keeping app 12-factor compliant

## API Contracts

### WebSocket (for real-time chat)

- **Connect**: `/ws/conversations/:id`
- **Protocol**: JSON messages, event-based.

**Sample Payloads:**

```json
// Client -> Server
{ "type": "user_message", "content":"..." }

// Server -> Client
{ "type": "delta", "content": "..." }
{ "type": "bot_message", "message_id": "...", "content": "..."}
```

### REST Endpoints (Draft)

| Method | Path  | Description |
| -- | -- | -- |
| POST | `/api/auth/login` | Login, returns JWT |
| POST | `/api/auth/signup` | Create user |
| GET | `/api/projects` | List projects |
| POST | `/api/projects` | Create project |
| GET | `/api/projects/:id` | Get project details |
| PUT | `/api/projects/:id` | Update project |
| DELETE | `/api/projects/:id` | Delete project |
| GET | `/api/projects/:id/files` | List files in project |
| GET | `/api/projects/:id/files/:id | View project file details |
| POST | `/api/projects/:id/files` | Upload file (multi) |
| GET | `/api/projects/:id/conversations | List all conversations associated with a specific project |
| GET | `/api/projects/:id/conversations/:id | View a specific conversation within a project |
| GET | `/api/conversations` | List all conversations |
| GET | `/api/conversations/:id` | Get conversation details |
| GET | `/api/download/files/:file_id` | Download file |
| GET | `/api/download/conversations/:id | Download conversation |
| GET | `/api/health` | Health check |

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

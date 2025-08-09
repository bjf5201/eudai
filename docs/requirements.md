# eudai - Requirements (EARS Notation)

## Ubiquitous

- THE SYSTEM SHALL have a server written in Python.
- THE SYSTEM SHALL have a client written using TypeScript with a Bun runtime environment.
- THE SYSTEM SHALL be deployable locally via Docker Compose using a multi-container architecture for Server, client, LLM (Ollama), and database.
- THE SYSTEM SHALL provide both a Web UI (React) and a CLI/TUI (Commander/Chalk) for interacting with the chatbot and knowledge management features. The CLI/TUI will be included in the MVP, the Web UI will be added to the project roadmap/backlog.
- THE SYSTEM SHALL persist user conversations, file uploads, and project metadata in a PostgreSQL database.

## Event-driven

- WHEN a user creates a new project, THE SYSTEM SHALL enable associating conversations, files, and URLs with that project.
- WHEN a user uploads a file, THE SYSTEM SHALL securely store the file and link it to the selected conversation/project.
- WHEN a user references a URL, THE SYSTEM SHALL associate the reference with a specific project or conversation.
- WHEN a user initiates a chat, THE SYSTEM SHALL route prompts through the Server to the DeepSeek model via Ollama and return results.
- WHEN a user initiates a chat, THE SYSTEM SHALL persist all turns/messages in the database, linked to the correct project.

## State-driven

- WHILE a conversation , THE SYSTEM SHALL persist all turns/messages in the database, linked to the correct project.
- WHILE the Server or client is initializing, THE SYSTEM SHALL retry LLM/DB connectivity until healthy or until a timeout is reached.
- WHILE running in the terminal, provide the end user an intuitive TUI which is intuitive to navigate and pleasant to look at.

## Unwanted

- IF a file upload fails, THEN THE SYSTEM SHALL return an error and not associate the file with the project.
- IF Ollama or the model is unavailable, THEN THE SYSTEM SHALL return a user-friendly error and log the incident.
- IF the database is unreachable, THEN THE SYSTEM SHALL serve a maintenance or error page and log the incident.

## Optional

- WHERE GPU support is available and enabled, THE SYSTEM SHALL run Ollama and DeepSeek using GPU acceleration.

## Complex

- WHEN running in Docker, THE SYSTEM SHALL allow switching between CPU and GPU modes via compose files or bash scripts.
- WHEN scaling up for multiple users, THE SYSTEM SHALL support multi-user authentication and authorization (future/optional).
- WHEN using the TUI, ensure the user has the same abilities as when they are using the web app.

---

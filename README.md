# eduai

Conversation-based, privacy-focused chatbot built for tech enthusiasts who want to deload menial tasks in order to focus on more complex or creative tasks.

## Features

- AI chatbot (Deepseek model via Ollama)
- Can be used via a self-hosted webapp OR your CLI
  - Deploy the webapp with quick Docker Compose command
  - Deploy the CLI with quick npm/pnpm/bun/yarn command
- Organize your tasks/thoughts via workspaces (coming soon)
- Agent-based tasks (coming soon)

## Philosophy

Based on the Greek word *eudaimonia* (εὐδαιμονία) which literally translates to *good spirit* or *being in good fortune*. It comes from a combination of "eu" ("good, well") and "daimōn" (a "spirit", or a "guiding force").

In ancient Greek philosophy, it referred to **human flourishing**. Aristotle referred to eduaimonia in reference to living well, or achieving the *highest form of happiness*.

Conveniently, `eudai` happens to also end with the letters **ai**, so, there's that :+1:.

## Roadmap

1. Workspaces
2. Agents
3. Account Signups? (If there is a demand for it.)

## Documentation

See the main [documentation here](./docs/design.md). Check out some of the decisions made so far below (which are also located in the main documentation).

<!-- ADR_START -->
## Architecture Decision Records (ADRs)

- [Ollama as distinct service](2025/08/2025-08-06-ollama-as-distinct-service.md)
- [Docker Compose vs Kubernetes](2025/08/2025-08-09_docker-compose-vs-kubernetes.md)
- [index](index.md)
<!-- ADR_END -->

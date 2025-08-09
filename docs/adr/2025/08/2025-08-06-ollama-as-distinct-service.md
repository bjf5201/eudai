# Decision - 2025-08-06 00:31:42 UTC

Ollama as distinct service

## Decision

**Ollama will be deployed as a distinct service container**, not bundled within the server backend image.

## Context

The `eudai` application requires an LLM backend (DeepSeek via Ollama) accessible to the FastAPI server. There are two main deployment models:

- Bundle Ollama and DeepSeek model within the server backend image/container.
- Deploy Ollama as a separate service container, exposing an HTTP API for the server to consume.
- **Reference**: [Recodify's `deepseek-r1-local-docker`](https://github.com/Recodify/deepseek-r1-local-docker/blob/master/scripts/setup-gpu.sh) repo also uses the distinct service model.

## Options

1. **Bundled approach**: Server and Ollama run in the same image/container.
    - *Pros*: Simpler single-container deployment, potentially easier local development.
    - *Cons*: Larger, more complex images; difficult to optimize resource usage; harder to update/scale LLM separately; more difficult to support CPU/GPU switching.

2. **Distinct service (selected option)**: Ollama is a separate image/container, orchestrated via Docker Compose.
    - *Pros*: Clear separation of concerns; easier to update/scale/troubleshoot the LLM; can independently manager server and LLM versions; aligns with industry best practices for microservices; simplifies multi-platform support (CPU/GPU).
    - *Cons*: Slightly more complex orchestration; containers must communicate over the network.

## Rationale

- Matches industry-standard microservice architecture for ML/LLM workloads.
- Simplifies upgrades, resource allocation, scaling, and platform-specific (CPU/GPU) deployment.
- Eases troubleshooting (clearer logs, isolation of concerns).
- Enables the `eudai` backend to be language-, version-, and platform-agnostic with respect to the LLM.

## Impact

- The `docker-compose.yml` will always define `ollama` as a separate service.
- The `server` (FastAPI) container will communicate with Ollama via HTTP (e.g., `OLLAMA_BASE_URL=http://ollama:11434`).
- The server image will be smaller, more secure, and easier to maintain.
- Ollama updates (including model/GPU support) can be managed independently and tested by several (potentially hundreds of) other developers.

## Review

- Revisit if a use case emerges for a single-binary or single-container deployment (e.g., for edge, serverless, or embedded scenarios).
- Review if Docker Compose orchestration proves problematic for users.
- Next review scheduled for major eudai version (v2.0) or upon user feedback about deployment quality or complexity.

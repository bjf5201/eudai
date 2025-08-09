# Decision - 2025-08-09 16:24:36 UTC

Docker Compose vs Kubernetes

## Decision

**Adopt Docker Compose as the primary container orchestration/development solution** for local development and single-node deployments. Defer Kubernetes support for advanced, production-grade, or multi-node deployment scenarios

## Context

- The application is intended for both CLI and web use, appealing to tech-savvy users who may want to run the app locally, self-host, or possibly scale to a private server.
- The stack includes Python (backend), PostgreSQL, and an LLM model (Deepseek via Ollama), requiring multi-container orchestration.
- Target users are comfortable with Docker, but not necessarily with full Kubernetes stack management.
- Goal: Keep onboarding friction low while leaving room for advanced deployment if needed.

## Options

1. **Docker Compose**
    - Pros:
        - Simple, fast onboarding for development and self-hosting.
        - Easy to run locally or on a single VM.
        - Ubiquitous among devs and self-hosters.
        - Lower resource footprint than Kubernetes.
        - Compose files can be converted to Kubernetes manifests later.
    - Cons:
        - Not suitable for high-availability, distributed, or auto-scaling use-cases.
        - Lacks advanced features like rolling updates, service mesh, etc.

2. **Kubernetes**
    - Pros:
        - Scalable, production-grade orchestration.
        - Advanced features (auto-scaling, rolling updates, secrets management).
        - Portable across major cloud vendors.
    - Cons:
        - High learning curve, especially for local/dev environments.
        - Overkill for most single-user or small-team deployments.
        - More complex setup for CLI-based or casual/local usage.

## Rationale

- Docker Compose offers the best developer and local user experience—easy to set up, widely understood, and well-documented.
- Most users will not need the complexity or operational overhead of Kubernetes for running the app as a local assistant or small self-hosted web service.
- Kubernetes can be supported later for those who want to run in a cloud-native/production environment (Helm charts or Kompose can help convert Compose files).
- Compose enables rapid prototyping and onboarding, aligning with the "get started fast" and "focus on creative work" value proposition.

## Impact

- Lower complexity for both development and user onboarding.
- Faster iteration cycles.
- Kubernetes support can be added later as a deployment target (not a blocker for core functionality).
- Documentation will focus on Docker Compose for local/dev and provide guidance for advanced/production deployments as a future enhancement.

## Review

- Revisit this decision when:
  - There is demand for cloud-native, scalable, or distributed deployment.
  - The application needs to support multi-node or high-availability use-cases.
  - User feedback indicates a significant portion of the audience prefers Kubernetes.

---

**Migration Path:**

- Compose files should be structured for easy conversion to Kubernetes manifests using tools like [Kompose](https://kompose.io/).
- When production scaling or multi-node orchestration is needed, implement Helm charts and Kubernetes manifests based on the existing Compose structure.

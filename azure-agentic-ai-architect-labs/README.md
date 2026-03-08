# Azure Agentic AI Architect Labs

This repository is being reset into a credible Azure-first learning and reference repo for agentic AI. As of March 8, 2026, the repo is in a **week-one stabilization state**:

- the folder structure is now documented explicitly
- module maturity is tracked in [MODULE-STATUS.md](./MODULE-STATUS.md)
- the recommended starting point is the module 09 golden path
- broad production-ready claims have been removed until the evidence exists

## What This Repo Is

This repo is intended to become:

- a structured learning path for Azure agentic AI labs
- a reference implementation for a secure, Azure-native agent workflow
- a delivery accelerator for architecture, security, and operations discussions

## Current Maturity

The repo is **not yet a full enterprise-grade reference implementation**. It currently has:

- one prioritized golden path in [09-end-to-end-reference-implementation](./09-end-to-end-reference-implementation/README.md)
- draft modules for the broader curriculum
- partial Bicep assets and sample app code
- baseline GitHub hygiene and validation workflows

See [MODULE-STATUS.md](./MODULE-STATUS.md) for the current truth.

## Start Here

Use this order:

1. Read [QUICK-START.md](./QUICK-START.md)
2. Review [REFERENCE-ARCHITECTURE.md](./REFERENCE-ARCHITECTURE.md)
3. Run the module 09 validation path in [09-end-to-end-reference-implementation](./09-end-to-end-reference-implementation/README.md)
4. Use [docs/repo-map.md](./docs/repo-map.md) to navigate the rest of the repo

## Repository Layout

```text
.
├── 01-foundry-foundations/
├── 02-foundry-agent-service/
├── 03-semantic-kernel-track/
├── 04-agent-framework-and-multi-agent/
├── 05-rag-with-azure-ai-search/
├── 06-mcp-and-enterprise-tooling/
├── 07-secure-reference-architecture/
├── 08-observability-and-evaluation/
├── 09-end-to-end-reference-implementation/
├── .github/
├── docs/
├── MODULE-STATUS.md
├── QUICK-START.md
├── REFERENCE-ARCHITECTURE.md
└── ARCHITECTURE.md
```

## Recommended Learning Path

The intended learning sequence is:

1. Foundry foundations
2. Foundry agent service
3. Semantic Kernel patterns
4. Multi-agent orchestration
5. RAG with Azure AI Search
6. MCP and enterprise tooling
7. Secure reference architecture
8. Observability and evaluation
9. End-to-end reference implementation

Only module 09 is currently positioned as the recommended execution path.

## What Works Today

Current week-one baseline:

- a truthful top-level README and quick start
- a documented module maturity view
- a single reference architecture for the current golden path
- a PowerShell validation script for module 09
- basic GitHub workflow, CODEOWNERS, issue templates, and PR template

## What Is Still In Progress

- standardizing each module README to the same template
- expanding infrastructure as code beyond the current baseline
- adding security, governance, observability, and evaluation artifacts at enterprise depth
- separating learning labs from the future enterprise reference track more cleanly

## Support Boundary

This repository should currently be treated as:

- safe for learning and repo modernization work
- useful for architecture discussion and pattern exploration
- **not yet sufficient as a production deployment standard without further hardening**

## Key Documents

- [QUICK-START.md](./QUICK-START.md)
- [MODULE-STATUS.md](./MODULE-STATUS.md)
- [REFERENCE-ARCHITECTURE.md](./REFERENCE-ARCHITECTURE.md)
- [ARCHITECTURE.md](./ARCHITECTURE.md)
- [09-end-to-end-reference-implementation/README.md](./09-end-to-end-reference-implementation/README.md)
- [docs/repo-map.md](./docs/repo-map.md)
- [docs/terminology.md](./docs/terminology.md)

## Immediate Next Steps

- make module 09 the fully validated golden path
- standardize the remaining modules to the same setup/run/validate/teardown template
- add Bicep environment overlays and a non-prod deployment workflow
- add security and governance artifacts before restoring stronger readiness claims

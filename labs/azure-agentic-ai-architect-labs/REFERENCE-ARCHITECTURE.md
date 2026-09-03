# Reference Architecture

This document defines the **current canonical architecture** for the repo. It is intentionally narrow and centered on module 09.

## Purpose

The reference path demonstrates how to evolve from a learning repo toward a defendable Azure-native agentic AI architecture with:

- one orchestrated agent workflow
- one retrieval pattern
- one infrastructure baseline
- one validation path

## Current Golden Path

The current golden path is:

- [09-end-to-end-reference-implementation](./09-end-to-end-reference-implementation/README.md)

## Logical Architecture

```text
User or tester
   |
   v
Python agent application
   |
   +--> Azure-hosted chat model
   |
   +--> Azure AI Search retrieval path
   |
   +--> enterprise tool adapters
   |
   \--> test and validation harness
```

## Azure Service Direction

The repo is converging on these Azure choices:

- Azure AI Foundry and Azure-hosted models for LLM execution
- Azure AI Search for RAG
- Azure API Management for future tool mediation
- Managed Identity instead of long-lived secrets wherever possible
- Key Vault for secret storage in production-shaped deployments
- Application Insights and Azure Monitor for future observability

## Trust Boundaries

The intended trust boundaries are:

1. user request boundary
2. application orchestration boundary
3. model invocation boundary
4. retrieval boundary
5. external tool boundary

The highest-risk boundary is the external tool boundary. That is why future hardening will prioritize tool mediation, authorization, and auditability.

## Current Reality

The current repo baseline does **not** yet fully enforce:

- private networking
- policy-as-code
- managed identity everywhere
- complete observability
- release-gated evaluations

Those items remain roadmap work and should not be implied by documentation.

## Recommended Week-One Standard

Use this standard until the repo matures further:

- one golden path
- truthful docs
- local validation first
- infrastructure validation second
- enterprise claims only where backed by code and artifacts

## Required Follow-On Artifacts

The next architectural artifacts to add are:

- `SECURITY.md`
- `THREAT-MODEL.md`
- `GOVERNANCE.md`
- `OPERATIONS.md`
- `FINOPS.md`
- `DECISIONS/ADR-001-iac-standard-bicep.md`

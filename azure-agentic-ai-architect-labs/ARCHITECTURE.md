# Architecture Decision Records (ADR) & Design Matrix

## 1. Solution Selection: Copilot Studio vs. Azure AI Foundry
This repository utilizes **Azure AI Foundry** precisely because it demonstrates a deterministic, code-first multi-agent workload that must communicate through an API Mediation Layer to mutate backend enterprise data systems safely. 

**Decision Matrix for the Enterprise:**

| Capability | Microsoft Copilot Studio (SaaS) | Azure AI Foundry + Semantic Kernel / Projects SDK (PaaS) |
| :--- | :--- | :--- |
| **Primary Persona** | Low-Code/No-Code Makers | Lead Developers & AI Engineers |
| **Speed to Value** | High (Minutes/Hours) | Medium (Days/Sprints) |
| **Control Boundary** | Declarative | Deterministic Code |
| **Tool Execution** | Out-of-the-box Graph connectors | Explicit OpenAPI / Custom SDK mediation |
| **Agentic Pattern** | Single Assistant (mostly) | Multi-Agent Coordinator/Worker Orchestration |
| **Cost Profile** | License Driven | Consumption (Token) Driven |
| **Ideal Use Case** | M365 Q&A, Standard HR workflows | Complex autonomous research, zero-trust CRM mutations |

## 2. The API Mediation Layer (Zero-Trust Standard)
**Context:** Generative AI components should never possess direct mutating privileges against source-of-truth databases.
**Implementation:** `09-end-to-end-reference-implementation/infra/main.bicep` deploys Azure APIM. The Python Foundry Agent invokes the `crm-integration-tool`, which is explicitly coded to pass HTTP REST commands *through* standard APIM endpoints rather than direct DB network access. APIM strips/verifies Entra tokens, rate limits the agent, and ensures safety constraints regardless of the LLM prompt output.

## 3. FinOps & Model Downgrades
**Context:** Relying entirely on `gpt-4o` wastes capital for low-level formatting tasks.
**Implementation:** In `agent-service.py`, the AI Project assigns `gpt-4o` to the `Coordinator Agent` for intent evaluation, but delegates exact data extraction tasks to the `Worker Agent` running `gpt-4o-mini`, cutting token costs by 10x per transaction.

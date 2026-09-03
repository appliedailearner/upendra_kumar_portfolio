# The 60-Day Microsoft Architecture Learning Path (AB-100 Focus)

## Month 1: The Core Frameworks & Solution Selection
*L67s do not speak in features; they speak in frameworks and governance. You must internalize the Microsoft Agentic AI strategy (AB-100).*

### Week 1: AB-100 Scope, Business Architecture & Landing Zones
*   **Goal:** Understand the business-solution scope and base infrastructure of an Agentic AI Architect.
*   **Action:** Read the official `AB-100 Study Guide`. Then, study the [Azure/azure-openai-landing-zone](https://github.com/Azure/azure-openai-landing-zone) reference architecture to understand how to deploy hub-and-spoke VNETs for secure AI.
*   **Key Concept:** Planning AI-powered business outcomes, ROI baselining, and evaluating adoption risk through secure Azure Landing Zones.

### Week 2: Platform Choice (Copilot vs Foundry)
*   **Goal:** Learn exactly when to recommend SaaS vs PaaS to CxOs.
*   **Action:** Study the Microsoft Copilot Studio documentation vs the Microsoft Foundry documentation. Watch *Azure AI for Developers: Building AI Agents* (LinkedIn).
*   **Key Concept:** Differentiating between low-code declarative agents and high-code deterministic workflow pipelines.

### Week 3: Grounding & Enterprise RAG
*   **Goal:** Master the absolute foundation of trusted AI.
*   **Action:** Deploy the industry-standard official Microsoft accelerator: [Azure-Samples/azure-search-openai-demo](https://github.com/Azure-Samples/azure-search-openai-demo) to understand vector architecture, hybrid search, and chunking strategies.
*   **Key Concept:** Grounding LLM responses entirely on authenticated, internal enterprise knowledge (RAG strategy).

### Week 4: Multi-Agent Orchestration & Code
*   **Goal:** Understand how agents delegate tasks.
*   **Action:** Clone and study Microsoft's advanced Agentic orchestrators: [microsoft/skmultiagents](https://github.com/microsoft/skmultiagents) and the [Azure/multi-agent-doc-research](https://github.com/Azure/multi-agent-doc-research) framework.
*   **Key Concept:** Coordinator and Worker agent patterns. Decomposing complex logic instead of using mega-prompts.

---

## Month 2: Scale, Governance, and Integration

### Week 5: Interoperability (MCP & A2A)
*   **Goal:** Understand open standards for Agentic communication.
*   **Action:** Study the Model Context Protocol (MCP) and Agent2Agent (A2A) paradigms. Review QA's "Orchestrate Agents with Microsoft Foundry Workflows" lab.
*   **Key Concept:** Agents must be able to securely talk to other agents across different clouds or domains.

### Week 6: The API Mediation Layer
*   **Goal:** Securely connecting agents to enterprise tools.
*   **Action:** Architect an integration pattern wrapping Azure Functions behind API Management for LLM tool-calling. Work through the official [Azure AI Gateway Labs](https://github.com/Azure-Samples/AI-Gateway/tree/main/labs/azure-ml-models).
*   **Key Concept:** Zero-trust architecture. Never letting an AI directly mutate a production system without an auditable gateway.

### Week 7: Security, Governance & Observability
*   **Goal:** Making Agentic AI regulator-ready.
*   **Action:** Deep dive into Azure AI Content Safety, Entra ID integration for AI models, Key Vault, and Application Insights for token tracking.
*   **Key Concept:** Private linking Azure OpenAI endpoints to keep enterprise telemetry off the public internet.

### Week 8: Evaluating Quality & Operating Models
*   **Goal:** Proving the AI is actually working post-deployment.
*   **Action:** Learn Azure Foundry Evaluation frameworks. Define support models (L1/L2) for AI systems.
*   **Key Concept:** AI architecture doesn't stop at deployment. You must benchmark groundedness, latency, and system safety daily.

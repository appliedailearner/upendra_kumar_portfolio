# Director-Level System Design Framework: Agentic AI 

When asked to whiteboard an Agentic architecture at Microsoft L67, use this structured framework mapped to the **AB-100 Agentic AI Reference Architecture**.

## Step 1: Clarify the Business & Evaluation Requirements (5 Mins)
1. **Business Goal:** Are we optimizing for human-in-the-loop co-piloting or fully autonomous background agents? Is this a Copilot Studio use case or a custom Azure AI Foundry build?
2. **Quality & Safety:** How will we evaluate "groundedness" and safety? What is the acceptable threshold for hallucination?
3. **Resiliency:** What is the required RTO and RPO for the semantic cache? 

## Step 2: The Agentic Reference Architecture (5 Mins)
Draw the 5 conceptual layers of the Microsoft Agentic AI Architecture:
1. **Experience Layer** (Teams, Custom UI, Copilot Studio frontend).
2. **Agent Orchestration Layer** (Semantic Kernel, Semantic Router, Planner agent vs Worker agent).
3. **AI Services Layer** (Azure OpenAI, Azure AI Search, Semantic Cache).
4. **Enterprise Integration Layer** (APIM, Azure Functions, ERP, Model Context Protocol [MCP]).
5. **Governance & Observability Layer** (Entra ID, Key Vault, Content Safety, App Insights).

## Step 3: Map to Azure Services (10 Mins)
Translate the abstract design into specific, enterprise-grade Azure PaaS.
*   **Orchestration:** Semantic Kernel hosted on Azure Kubernetes Service (AKS) or Azure Container Apps for multi-agent coordination.
*   **Grounding (RAG):** Azure AI Search with Hybrid Search and Semantic Ranking enabled for superior vector match quality.
*   **Integration:** Azure API Management acting as the sole gateway for LLM tool-calling (The API Mediation Layer).
*   **Observability:** Application Insights tracking token telemetry and latency across distributed tracing. 

## Step 4: The L67 Differentiators (15 Mins)
This is where you prove you are a Director, not just an Engineer. You must proactively discuss:
1.  **Stop Using Single Agents:** "For this complex supply chain task, a single agent will hallucinate. I will decompose this into a Multi-Agent workflow: a Coordinator agent, a Researcher worker agent, and a Validator (Evaluator) agent."
2.  **The API Mediation Layer:** "I will never connect the Semantic Kernel tool executor directly to the database. We will route all tool calls through APIM to enforce RBAC, logging, and zero-trust."
3.  **Evaluating Quality (MLOps/LLMOps):** "Architecture does not end at deployment. We will implement ongoing AI evaluation pipelines to track Groundedness, Relevance, and Coherence metrics to detect model drift over time."
4.  **Responsible AI Integration:** "We will insert Azure AI Content Safety at the perimeter to filter prompt injection attacks and toxic outputs before they ever hit the LLM."

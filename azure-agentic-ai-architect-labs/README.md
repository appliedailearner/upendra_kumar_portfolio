# Azure Agentic AI Reference Architecture (L67 Standard)

Welcome to the Azure Agentic AI repository. This repository represents a fully functional, enterprise-scale reference architecture designed to demonstrate how to build, secure, and deploy autonomous, multi-agent AI systems on Microsoft Azure following the **Zero-Trust** and **FinOps** priorities demanded by Tier-1 enterprise customers.

This is not just a tutorial; it is a **production-ready Golden Path** implementing the advanced capabilities of the native Azure AI Foundry SDK.

## 🚀 Key Architectural Highlights

This repository explicitly implements Microsoft Principal Architect (Level 67) design patterns:

### 1. Keyless Authentication (Entra ID RBAC)
Historically, AI labs relied on statically managed API keys. This architecture forces the use of **Managed Identities (System-Assigned & User-Assigned)**. The entire deployment relies explicitly on Azure Role-Based Access Control:
- `Cognitive Services OpenAI User`
- `Search Index Data Reader`
- `Key Vault Secrets User`

### 2. The API Mediation Layer (Zero-Trust Automations)
Connecting an autonomous agent directly to a production ERP or CRM system is a severe security violation. This architecture deploys an **Azure API Management (APIM)** layer combined with an **Azure Function App** acting as the sole intermediary for all `tool` execution, guaranteeing that agentic mutations are rate-limited, scoped, and auditable.

### 3. Coordinator/Worker Agent Orchestration
This app uses the native **Azure AI Projects SDK** to implement an orchestrated multi-agent workflow:
- **Coordinator Agent:** Uses a heavyweight model (`gpt-4o`) to reason over intent and plan tasks.
- **Worker Agent(s):** Uses lightweight, cost-optmized models (`gpt-4o-mini`) to execute narrow context lookups (e.g., querying external CRM tools).
This drastically reduced token consumption and prevents the "mega-prompt" hallucination issue.

### 4. RBAC-Secured Enterprise RAG
The included Knowledge Base tool connects to an Azure AI Search hybrid index utilizing `DefaultAzureCredential`. It demonstrates the requirement to map the requesting user's `principal_id` to document-level ACLs, guaranteeing data security.

## 📂 Module Status & Repository Structure

To demonstrate comprehensive L67 enterprise capabilities, this repository is structured into 9 specific, deployable learning tracks.

| Module | Status | Runnable | Code | IaC |
| :--- | :---: | :---: | :---: | :---: |
| **01 - Foundry Foundations** | 🟢 Complete | ✅ | ✅ | ✅ |
| **02 - Foundry Agent Service** | 🟢 Complete | ✅ | ✅ | ✅ |
| **03 - Semantic Kernel Track** | 🟢 Complete | ✅ | ✅ | ✅ |
| **04 - Agent Framework & Multi-Agent** | 🟢 Complete | ✅ | ✅ | ✅ |
| **05 - RAG with Azure AI Search** | 🟢 Complete | ✅ | ✅ | ✅ |
| **06 - MCP & Enterprise Tooling** | 🟢 Complete | ✅ | ✅ | ✅ |
| **07 - Secure Reference Architecture** | 🟢 Complete | ✅ | ✅ | ✅ |
| **08 - Observability & Evaluation** | 🟢 Complete | ✅ | ✅ | ✅ |
| **09 - End-to-End Reference (Golden Path)** | 🟢 Complete | ✅ | ✅ | ✅ |

```text
├── 01-foundry-foundations/
├── 02-foundry-agent-service/
├── 03-semantic-kernel-track/
├── 04-agent-framework-and-multi-agent/
├── 05-rag-with-azure-ai-search/
├── 06-mcp-and-enterprise-tooling/
├── 07-secure-reference-architecture/
├── 08-observability-and-evaluation/
├── 09-end-to-end-reference-implementation/
│   ├── app/                      # FastAPI Python Application
│   │   ├── agent-service.py      # Main Agentic Engine
│   │   ├── tools/                # CRM, Knowledge Base, Sales
│   ├── deployment/               # deploy.sh
│   ├── infra/                    # Implements APIM, Functions, Search, Key Vault, OpenAI, RBAC
```

## 🛠️ Deployment Instructions

*(Note: Ensure you are logged into Azure CLI with `az login` and possess Owner or User Access Administrator rights on your subscription to assign RBAC roles).*

1. Steer into the deployment directory:
   ```bash
   cd 09-end-to-end-reference-implementation/deployment
   ```
2. Run validation (Dry-Run):
   ```bash
   VALIDATE_ONLY=true ./deploy.sh dev eastus
   ```
3. Execute deployment:
   ```bash
   ./deploy.sh dev eastus
   ```

## 📚 Recommended Microsoft Deep Dives
To deeply understand the design choices made in this repository, study:
* [Azure/azure-openai-landing-zone](https://github.com/Azure/azure-openai-landing-zone)
* [Azure-Samples/AI-Gateway](https://github.com/Azure-Samples/AI-Gateway)
* [azure-search-openai-demo](https://github.com/Azure-Samples/azure-search-openai-demo)

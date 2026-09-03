# 🏛️ Director-Level Reference Architecture Diagrams (AB-100)

As a Level 67/68 Architect, you are expected to understand the official Microsoft topologies for enterprise scale. Use these official Azure Architecture Center and GitHub references to study the exact diagrams. 

When you whiteboard during an interview, your drawings should closely mirror these official patterns.

---

## 1. The API Mediation Layer (AI Gateway)
*   **Goal:** Protect backend AI models from direct access. Enforce zero-trust token logging, rate limiting, and OAuth 2.0 validation using Azure API Management (APIM).
*   **Official Pattern:** [Accessing Azure OpenAI through a Gateway (Microsoft Learn)](https://learn.microsoft.com/en-us/azure/architecture/ai-ml/architecture/azure-openai-api-management)
*   **Code & Architecture Repo:** [Azure-Samples/genai-gateway-apim](https://github.com/Azure-Samples/genai-gateway-apim)
*   **Key Whiteboard Elements:** Always draw the Client interacting with APIM *first*, which then routes to a backend Azure Function or direct Azure OpenAI endpoint over Private Link. 

## 2. Multi-Agent Orchestration
*   **Goal:** Decompose a massive monolithic LLM prompt into specialized, smaller agents (Coordinator and Workers) to prevent hallucination and reduce token costs.
*   **Official Pattern:** [Multi-Agent Orchestration with Semantic Kernel](https://learn.microsoft.com/en-us/semantic-kernel/frameworks/multi-agent)
*   **Code & Architecture Repo:** [Microsoft/skmultiagents](https://github.com/microsoft/skmultiagents)
*   **Key Whiteboard Elements:** Never draw one agent pointing to five tools. Draw the user hitting a 'Coordinator', which then fans out specialized tasks to 'Workers', culminating in an 'Evaluator' gate.

## 3. Enterprise RAG (Grounding & Vector Search)
*   **Goal:** The industry standard for injecting isolated enterprise documents into LLM prompts securely.
*   **Official Pattern:** [Azure Search OpenAI Demo Architecture](https://learn.microsoft.com/en-us/azure/architecture/example-scenario/ai/enterprise-knowledge-apps-with-azure-openai)
*   **Code & Architecture Repo:** [Azure-Samples/azure-search-openai-demo](https://github.com/Azure-Samples/azure-search-openai-demo)
*   **Key Whiteboard Elements:** Show vector embedding pipelines traversing from Azure Blob Storage to Azure AI Search, utilizing Hybrid Search (BM25 + Vectors) and Semantic Ranking before passing the context window back to GPT-4.

## 4. Azure OpenAI Enterprise Landing Zone
*   **Goal:** Network isolation. Prevent data leakage and manage massive organizational structure using Cloud Adoption Framework (CAF) principles.
*   **Official Pattern:** [Azure OpenAI Reference Architecture - Hub and Spoke](https://learn.microsoft.com/en-us/azure/architecture/ai-ml/architecture/azure-openai-landing-zone)
*   **Code & Architecture Repo:** [Azure/azure-openai-landing-zone](https://github.com/Azure/azure-openai-landing-zone)
*   **Key Whiteboard Elements:** Draw the VNET bounding boxes clearly. Emphasize Azure Private Endpoints for the Cognitive Services, ensuring no data traverses public IP space.

## 5. Planetary Scale: Active-Active Compute 
*   **Goal:** High-stress financial workloads demanding 50,000 TPS, zero data loss (RPO 0), and instant failover (RTO < 10 seconds).
*   **Official Pattern:** [Highly available multi-region AKS deployments](https://learn.microsoft.com/en-us/azure/architecture/reference-architectures/containers/aks-multi-region)
*   **Key Whiteboard Elements:** Draw Azure Front Door (Anycast) at the global edge. Route traffic to active-active Azure Kubernetes Service (AKS) clusters in paired regions. Bind the stateful persistence layer to a globally distributed Cosmos DB ring using multi-region writes.

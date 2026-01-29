# Master Prompt: Microsoft Azure Architecture Designer (Regulator-Ready Fortress Version)

Use this prompt to generate diagrams that strictly adhere to the **2D AAC Standard** and the **specific tech stack** described in the blog post.

---

## 1. Core Tech Stack (Regulator-Ready Fortress)

**DO NOT use App Service or App Service Plans.** The architecture is strictly AKS-based.

### 1. Global Connectivity & Security (The Outer Wall)
- **Azure Front Door Premium:** Global entry point with integrated WAF (Web Application Firewall) to filter malicious traffic.
- **Private Link Service (PLS):** The "Invisible Tunnel" that allows Front Door to talk privately to backend VNets without exposing Public IPs.

### 2. Core Networking (The Hub)
- **Hub VNet:** Central point of connectivity.
- **Azure Firewall:** Controls east-west/north-south traffic flow and enforces network policies.
- **VPN Gateway:** Provides secure connectivity from on-premises networks to the Azure Hub.
- **VNet Peering:** Connects the Hub VNet to the varied Spoke VNets.

### 3. Compute & Application Logic (The Engine)
- **Azure Kubernetes Service (AKS):** Primary compute cluster hosting application workloads in Spoke VNets.
- **Azure Application Gateway (AGIC):** Acts as the Ingress Controller within the Spoke VNet, routing traffic securely to AKS pods.

### 4. AI & Data Layers (The Crown Jewels)
- **Azure OpenAI Service (PTU):** Provisioned Throughput Units for guaranteed, private access to GPT models.
- **Azure AI Search:** Powered by Private Link, enabling secure retrieval operations (RAG).
- **Azure Cosmos DB:** Operational database accessed via Private Endpoint.
- **Azure SQL Database:** Structured data storage with Geo-Replication for DR.
- **Azure Redis Cache:** Semantic caching to reduce API costs and latency.
- **Private Endpoints:** The critical "network glue" connecting all PaaS services (OpenAI, Search, Cosmos, SQL) to the VNet.

### 5. Security & Identity (The Guardrails)
- **Azure API Management (APIM) - Dual Gateway Pattern:**
    - **External Gateway (Hub):** Authentication (mTLS), rate limiting, initial validation.
    - **Internal Gateway (Spoke):** AI-specific logic (PII masking, token throttling, semantic caching).
- **Microsoft Entra ID (Azure AD):** Identity provider, synchronized with on-prem AD via Entra Connect.
- **Azure Key Vault:** Securely manages secrets, keys, and certificates.
- **Azure Policy:** Enforces compliance (MCSB v2, NIST, PCI-DSS).

### 6. DevOps & Disaster Recovery
- **Azure Container Registry (ACR):** Stores container images with Geo-Replication (UK South <-> UK West).
- **Azure Monitor:** Full-stack observability and security logging.

### 7. Advanced / Day 2 Components (Evolution)
- **Microsoft Purview:** Unified data governance.
    - **Data Map:** Scans Private Endpoints (SQL, Cosmos) for PII.
    - **AI Hub:** Audits OpenAI prompt/completion logs for compliance.
- **Azure SRE Agent:** Autonomous operations agent.
    - **Role:** Monitors telemetry, auto-triages alerts, and executes remediation runbooks.
    - **Location:** Hosted in Management VNet.
- **MS Learn MCP Server:** Reliable knowledge source.
    - **Role:** Model Context Protocol (MCP) server providing grounded answers from Microsoft Learn.
    - **Pattern:** Sidecar or Microservice in AI Spoke.

---

## 2. Visual Style (AAC 2D)
- **2D Flat Symbolic Icons:** No 3D, no isometric, no gradients.
- **Orthogonal Connectors:** 90-degree lines only with clear arrowheads.
- **Background:** Pure White (#FFFFFF).
- **Typography:** Segoe UI text for all labels.
- **Boundaries:** Rounded rectangles with thin grey borders for VNets/Subnets.

## 3. Specific Diagram Requirements

### A. Solution Overview
- **Layout:** Central Hub VNet connected to multiple Spoke VNets.
- **Hub:** Azure Firewall, VPN Gateway, External APIM.
- **Spokes:** AKS Clusters, Internal APIM, Private Endpoints for OpenAI/Search/Cosmos.
- **Flow:** Traffic from Front Door -> PLS -> Hub -> Spokes.

### B. Network & Data Flow
- **Focus:** Path of a request.
- **Chain:** Front Door -> Private Link -> Azure Firewall -> VNet Peering -> AGIC -> AKS Pod -> Private Endpoint -> OpenAI.

### C. Security Perimeter
- **Focus:** Vault concept.
- **Highlight:** Entra ID, Key Vault, and Dual-Gateway APIM (External vs Internal).

### D. Service Journey Map
- **Steps:** 1. User -> 2. Front Door -> 3. External APIM (Hub) -> 4. Internal APIM (Spoke) -> 5. AKS/Inference -> 6. OpenAI/Data.

### E. DR Failover Journey
- **Layout:** Two regions (UK South/UK West).
- **State:** UK South (Primary/Active), UK West (Standby).
- **Sync:** SQL Geo-Replication, ACR Geo-Replication arrows.
- **Failover:** Front Door routing traffic path change to UK West.

---

## 4. Prompt Template
> "A 2D flat technical architecture diagram for the 'Regulator-Ready AI Fortress' following Microsoft Azure Architecture Center standards. Pure white background, Segoe UI text. Featured components: [LIST_SERVICE_NAMES_HERE]. Use official 2D Azure icons. Draw logical groupings as rounded rectangles. All connectors are orthogonal lines. Clean, professional, high-resolution documentation style."

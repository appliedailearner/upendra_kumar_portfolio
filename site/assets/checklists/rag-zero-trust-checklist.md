# RAG Zero Trust Checklist

Use this checklist to validate the security posture of your Azure RAG (Retrieval-Augmented Generation) implementation.

## 1. Network Isolation (The Foundation)
- [ ] **Hub-and-Spoke Topology**: Workload deployed in a dedicated Spoke VNet, peered to a Hub VNet.
- [ ] **No Public Endpoints**: All PaaS services (Azure OpenAI, AI Search, Storage, Key Vault, App Service) have public network access disabled.
- [ ] **Private Endpoints**: 
  - [ ] Azure OpenAI (`privatelink.openai.azure.com`)
  - [ ] Azure AI Search (`privatelink.search.windows.net`)
  - [ ] Storage Account (`privatelink.blob.core.windows.net`)
  - [ ] Key Vault (`privatelink.vaultcore.azure.net`)
- [ ] **Private DNS Zones**: All Private Endpoints are registered in the correct Private DNS Zones and linked to the VNet.
- [ ] **VNet Integration**: The App Service (or Container App) is VNet Integrated to reach the Private Endpoints.

## 2. Identity & Access Management (RBAC)
- [ ] **Managed Identity**: The App Service uses a System-Assigned Managed Identity.
- [ ] **No Keys in Code**: Connection strings use `Credential="ManagedIdentity"` (e.g., `DefaultAzureCredential`).
- [ ] **Least Privilege Roles**:
  - [ ] **Cognitive Services OpenAI User**: Assigned to the App Identity on the Azure OpenAI resource.
  - [ ] **Search Index Data Reader**: Assigned to the App Identity on the AI Search resource.
  - [ ] **Storage Blob Data Reader**: Assigned to the App Identity on the Storage container.
- [ ] **Admin Access**: Developers access resources via a Bastion Host or VPN, not public IP.

## 3. Egress Control & Data Exfiltration
- [ ] **Route Table (UDR)**: A User Defined Route (0.0.0.0/0) forces all outbound traffic to an Azure Firewall or NVA.
- [ ] **Allowlist Only**: Azure Firewall Application Rules allow only necessary FQDNs (e.g., `pypi.org` for build, specific APIs).
- [ ] **Deny by Default**: All other outbound traffic is blocked and logged.

## 4. Application Security & Evaluation
- [ ] **Input Validation**: User input is sanitized to prevent injection attacks.
- [ ] **Content Safety**: Azure AI Content Safety filters are enabled (Hate, Violence, Self-harm, Sexual) at "Medium" or "High".
- [ ] **System Prompt Hardening**: System prompt includes instructions to refuse revealing internal instructions.
- [ ] **Evaluation Harness**: An automated pipeline (e.g., Prompt Flow) runs on every commit to check for regression in groundedness.

## 5. Observability
- [ ] **Centralized Logging**: All resources send Diagnostic Settings (Logs & Metrics) to a central Log Analytics Workspace.
- [ ] **Audit Trails**: Azure Firewall logs and NSG Flow Logs are enabled and retained.
- [ ] **Application Insights**: Distributed tracing is enabled to correlate user requests with backend dependency calls.

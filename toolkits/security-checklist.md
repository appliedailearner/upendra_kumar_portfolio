# 🛡️ Azure AI Hosting: "Go-Live" Security Checklist

## 1. Network Security (Zero Trust)
- [ ] **Private Endpoints Enabled:** Ensure `public_network_access_enabled` is set to `false` for Azure OpenAI resource.
- [ ] **DNS Resolution:** Verify `privatelink.openai.azure.com` resolves to a private IP within your VNet.
- [ ] **VNet Integration:** Ensure the hosting compute (Container Apps/AKS) is injected into the VNet.
- [ ] **NSG Rules:** Limit inbound traffic to the APIM subnet only.

## 2. API Gateway (APIM)
- [ ] **Managed Identity:** APIM uses System-Assigned Managed Identity to authenticate with Azure OpenAI (Keyless auth).
- [ ] **Rate Limiting:** `rate-limit-by-key` policy is active for all AI routes.
- [ ] **JWT Validation:** `validate-jwt` policy enforces Entra ID (AAD) authentication.
- [ ] **Logging:** `azure-openai-emit-token-metric` policy is enabled to track token usage per user.

## 3. Container Security
- [ ] **Image Vulnerability Scanning:** Enable Defender for Containers on the Container Registry (ACR).
- [ ] **Secret Management:** No API keys in environment variables; use Key Vault references.
- [ ] **Egress Control:** Restrict outbound traffic to only required services (Azure OpenAI, Storage) via Firewall.

## 4. Operational Excellence
- [ ] **Cost Alerts:** Budget alerts set for Azure OpenAI resource (at 50%, 80%, 100%).
- [ ] **Diagnostic Settings:** Audit logs sent to Log Analytics Workspace.

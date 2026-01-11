# Azure AI Hosting Decision Tree - Implementation Toolkit

## 📦 What's Inside

This toolkit provides production-ready Terraform templates, APIM policies, and architecture diagrams to implement the five scenarios from the "Pick the Wrong Compute, Pay Forever" blog post.

### Contents

```
ai-hosting-toolkit/
├── README.md (this file)
├── scenarios/
│   ├── 01-internal-only/          # Private-only agents (regulated enterprise)
│   ├── 02-public-entry/           # Internet-facing customer AI
│   ├── 03-hybrid/                 # Azure runtime + on-prem tools
│   ├── 04-gpu/                    # GPU skills without AKS platform team
│   └── 05-batch/                  # Batch pipelines and offline jobs
├── policies/
│   ├── jwt-validation.xml         # Entra ID JWT validation
│   ├── token-quota.xml            # Token quota enforcement
│   ├── rate-limiting.xml          # Rate limiting per client
│   └── tool-allowlist.xml         # Tool API allowlisting
└── diagrams/
    ├── protect-apis.webp           # APIM gateway architecture
    ├── internal-apim.png          # Internal APIM pattern
    ├── landing-zone-networking.png # Landing zone networking
    ├── network-isolation.svg      # Network isolation
    └── basic-openai.png           # Basic OpenAI architecture
```

---

## 🚀 Quick Start

### Prerequisites

- **Azure CLI**: `az --version` (2.50.0+)
- **Terraform**: `terraform --version` (1.5.0+)
- **Azure Subscription**: With Contributor access
- **Entra ID**: Permissions to create App Registrations

### Step 1: Choose Your Scenario

| Scenario | Use When | Compute | Networking |
|----------|----------|---------|------------|
| **01-internal-only** | Employee copilots, regulated data | ACA | Private-only |
| **02-public-entry** | Customer chat, partner APIs | ACA | Public entry, private backend |
| **03-hybrid** | On-prem tool integration | ACA | ER/VPN required |
| **04-gpu** | Vision, embeddings, custom inference | ACA GPU | Flexible |
| **05-batch** | Backfills, nightly jobs | ACI/ACA Jobs | Flexible |

### Step 2: Deploy

```bash
# Navigate to your scenario
cd scenarios/01-internal-only

# Initialize Terraform
terraform init

# Review the plan
terraform plan -var-file="terraform.tfvars"

# Deploy
terraform apply -var-file="terraform.tfvars"
```

### Step 3: Apply APIM Policies

```bash
# Copy the policy XML from policies/ folder
# Apply via Azure Portal or Azure CLI

az apim api policy create \
  --resource-group <your-rg> \
  --service-name <your-apim> \
  --api-id <your-api-id> \
  --xml-policy-file ../policies/jwt-validation.xml
```

---

## 📋 Scenario Details

### Scenario 1: Internal-Only Agents

**When**: Employee copilots, internal knowledge agents, regulated data

**What It Deploys**:
- APIM in internal VNet mode (private gateway)
- Azure Container Apps in VNet-integrated environment
- Azure OpenAI with Private Endpoint + Private DNS
- Key Vault for secrets
- Application Insights for logging

**Critical Policies**:
- JWT validation (Entra ID)
- Token quota enforcement
- Tool allowlisting

**Estimated Cost**: ~$500-800/month (depends on usage)

---

### Scenario 2: Public Entry, Private Backend

**When**: Customer chat, partner agent APIs, public portals

**What It Deploys**:
- Application Gateway with WAF
- APIM as public API surface
- Azure Container Apps for runtime
- Private endpoints to model and data

**Critical Policies**:
- Token quota (mandatory)
- Bot/abuse throttling
- Request size limits

**Estimated Cost**: ~$700-1000/month (depends on traffic)

---

### Scenario 3: Hybrid Agents

**When**: Agent must call on-prem systems (CMDB, ITSM, legacy APIs)

**What It Deploys**:
- APIM in controlled network path to on-prem
- Azure Container Apps in same network boundary
- VPN Gateway or ExpressRoute connection
- Tool APIs behind allowlisted routes

**Critical Policies**:
- JWT validation
- Tool allowlisting (on-prem + cloud)
- Timeout configuration

**Estimated Cost**: ~$800-1200/month (includes ER/VPN)

---

### Scenario 4: GPU Skills

**When**: Vision, heavy embeddings, GPU bursts, custom inference

**What It Deploys**:
- APIM front door with quotas
- Azure Container Apps with serverless GPU workers
- Azure Container Registry (Premium)
- Private endpoints where required

**Critical Policies**:
- Token quota
- Request timeout (long-running)
- Retry logic

**Estimated Cost**: ~$1000-2000/month (GPU costs vary)

---

### Scenario 5: Batch Pipelines

**When**: Backfills, re-embedding runs, nightly summarization

**What It Deploys**:
- Azure Container Instances for CPU batch tasks
- Azure Storage for artifacts
- Application Insights for logging
- Azure Monitor for scheduling

**Critical Policies**:
- Idempotency enforcement
- Run metadata logging

**Estimated Cost**: ~$200-400/month (pay-per-run)

---

## 🛡️ Security Best Practices

### 1. Identity at the Gateway
✅ **DO**: Use `validate-jwt` or `validate-azure-ad-token` at APIM  
❌ **DON'T**: Distribute model API keys to client apps

### 2. Private Endpoints
✅ **DO**: Use Private Endpoints for model and data in production  
❌ **DON'T**: Leave public endpoints enabled "temporarily"

### 3. DNS Configuration
✅ **DO**: Configure Private DNS zones correctly from day 1  
❌ **DON'T**: Skip DNS planning—it causes weeks of rework

### 4. Egress Control
✅ **DO**: Define egress rules before deployment  
❌ **DON'T**: Use "allow all" and plan to restrict later

### 5. Token Quotas
✅ **DO**: Enforce per-client quotas at APIM  
❌ **DON'T**: Rely on model-level quotas alone

---

## 🔧 Customization Guide

### Modifying Terraform Variables

Each scenario has a `terraform.tfvars.example` file. Copy it to `terraform.tfvars` and customize:

```hcl
# terraform.tfvars
location            = "eastus2"
environment         = "prod"
project_name        = "ai-agents"
apim_sku            = "Developer"  # Change to Premium for production
aca_min_replicas    = 1
aca_max_replicas    = 10
openai_sku          = "S0"
enable_private_endpoints = true
```

### Adding Custom Policies

1. Copy a policy template from `policies/`
2. Modify the XML to match your requirements
3. Apply via Azure CLI or Portal

---

## 📊 Cost Optimization Tips

1. **Use ACA scale-to-zero**: Set `min_replicas = 0` for non-critical workloads
2. **Enable semantic caching**: Reduce token consumption by 40-60%
3. **Use APIM consumption tier**: For dev/test environments
4. **Right-size GPU**: Use T4 for inference, A100 only when needed
5. **Monitor and alert**: Set budget alerts at 80% threshold

---

## 🐛 Troubleshooting

### Issue: Private Endpoint DNS not resolving

**Solution**:
```bash
# Verify Private DNS zone is linked to VNet
az network private-dns link vnet list \
  --resource-group <rg> \
  --zone-name privatelink.openai.azure.com

# Check DNS resolution from ACA
az containerapp exec \
  --name <app-name> \
  --resource-group <rg> \
  --command "nslookup <your-openai>.openai.azure.com"
```

### Issue: APIM returns 401 Unauthorized

**Solution**:
- Verify JWT validation policy has correct `audience` and `issuer`
- Check Entra ID app registration has correct API permissions
- Ensure client is sending `Authorization: Bearer <token>` header

### Issue: ACA cold start too slow

**Solution**:
- Reduce container image size (use multi-stage builds)
- Use Premium Container Registry for faster pulls
- Set `min_replicas = 1` for critical workloads
- Pre-warm containers with health checks

---

## 📚 Additional Resources

### Official Documentation
- [Azure Container Apps](https://learn.microsoft.com/en-us/azure/container-apps/)
- [Azure API Management](https://learn.microsoft.com/en-us/azure/api-management/)
- [Azure OpenAI Service](https://learn.microsoft.com/en-us/azure/ai-services/openai/)

### Sample Repositories
- [AI Gateway Samples](https://github.com/Azure-Samples/AI-Gateway)
- [GenAI Gateway with APIM](https://github.com/Azure-Samples/genai-gateway-apim)
- [APIM + Azure OpenAI Reference](https://github.com/microsoft/AzureOpenAI-with-APIM)

### Blog Post
- [Pick the Wrong Compute, Pay Forever: Azure AI Hosting Decision Tree](https://portfolio.upendrakumar.com/blog/2026-01-11-ai-hosting-decision-tree.html)

---

## 🤝 Support

For questions or issues:
- **Blog Comments**: Leave a comment on the blog post
- **GitHub Issues**: (if you fork this toolkit)
- **Contact**: [Contact Upendra Kumar](https://portfolio.upendrakumar.com/pages/contact.html)

---

## 📄 License

This toolkit is provided as-is for educational and reference purposes. Modify as needed for your production requirements.

**Version**: 1.0.0  
**Last Updated**: 2026-01-11  
**Author**: Upendra Kumar

# Engineering Cross-Region Disaster Recovery for Azure API Management, AI Search, Document Intelligence, and AI Foundry: A Zero-Trust Architecture Field Guide

**Author:** Upendra Kumar, Cloud Solutions Architect  
**Published:** April 18, 2026 | **Updated:** April 19, 2026  
**Tags:** Architecture · Disaster Recovery · Risk Mitigation · Azure Front Door · NSG Lockdown · Zero Trust  
**Live Blog:** https://portfolio.upendrakumar.com/blog/2026-04-18-azure-apim-ai-foundry-dr-uae-sweden.html

---

> *"The board-level mandate is always identical: when UAE North fails, Sweden Central must instantly take over. The engineering reality? Azure API Management tiers and Generative AI scaling models do not fail over uniformly. Here is the authoritative blueprint for engineering the recovery gap."*

---

## Table of Contents

1. [The Scenario](#the-scenario)
2. [The First Hard Truth: APIM Tiers Matter](#the-first-hard-truth-apim-tiers-matter)
3. [Designing DR for AI Services](#designing-dr-for-ai-services)
   - [Azure AI Search — DR & Backup Engineering](#azure-ai-search--dr--backup-engineering)
   - [Azure Document Intelligence — DR & Backup Engineering](#azure-document-intelligence--dr--backup-engineering)
   - [Azure AI Foundry & Model Endpoints — DR & Backup Engineering](#azure-ai-foundry--model-endpoints--dr--backup-engineering)
   - [Azure API Management — Backup, Restore & DR Engineering](#azure-api-management--backup-restore--dr-engineering)
4. [Enterprise Landing Zone Engineering](#enterprise-landing-zone-engineering)
5. [APIM DR Alternatives at a Glance](#apim-dr-alternatives-at-a-glance)
6. [Engineer's Runbook: Deploying the DR Pattern](#engineers-runbook-deploying-the-dr-pattern)
7. [Front Door + APIM Origin Lockdown Pattern](#front-door--apim-origin-lockdown-pattern)
8. [The Traps to Avoid](#the-traps-to-avoid)
9. [References & Further Reading](#references--further-reading)

---

## The Scenario

Imagine an enterprise platform serving mobile apps, partner integrations, internal business systems, and AI-assisted workflows across the Middle East. The primary region is **UAE North**. It leverages Azure API Management (APIM) as the gateway tier, intertwined with Azure AI Search, Document Intelligence, and Azure AI Foundry endpoints.

The business mandates a strict disaster recovery design extending into **Sweden Central**. Simple geography, right? Wrong. The first issue is tier reality. APIM does not support identical DR mechanisms across its versions. The second issue is service behavior. Generative AI endpoint availability and failure patterns do not mirror traditional IaaS configurations. And the third issue? **UAE North to Sweden Central is an explicitly non-paired cross-geography DR design.**

If you assume an active-passive pattern is just a simple "networking flip", then your architecture looks fine in presentation slides, but completely fails under system pressure.

---

## The First Hard Truth: APIM Tiers Matter

Microsoft's reliability SLA is clear, yet often glossed over. Not every tier of APIM natively supports multi-region routing. Here is the operational reality check you need before finalizing any topology:

- **Premium classic** supports native **multi-region deployment**. But remember, this propagates gateway proxies, not isolated backup environments.
- **Premium v2** supports **availability zones**, but it entirely lacks multi-region deployments. Worse yet, as of current mappings, it is not even available in UAE North. Designing around a non-supported tier is an amateur mistake.
- **Standard v2** supports neither out-of-the-box.

### APIM Tier Comparison: DR Feature Matrix

> Source: [Azure APIM Feature Comparison](https://learn.microsoft.com/en-us/azure/api-management/api-management-features)

| Feature | Consumption | Developer | Basic v2 | Standard | Standard v2 ★ | Premium | Premium V2 |
|---|---|---|---|---|---|---|---|
| SLA | 99.95% | ✗ | 99.95% | 99.95% | **99.95%** | 99.99% | 99.99% |
| Max Scale-out | N/A | 1 | 10 | 4 | **10** | 10/region | 30 |
| VNet Support | ✗ | ✓ | ✗ | ✗ | **✓** | ✓ | ✓ |
| Multi-Region Deploy | ✗ | ✗ | ✗ | ✗ | **✗** | ✓ | ✗ |
| Self-hosted Gateway | ✗ | ✓ | ✗ | ✗ | **✓** | ✓ | ✗ |
| Custom Domain Names | ✗ | ✓ | ✗ | ✗ | **✓** | ✓ | ✗ |
| Developer Portal | ✗ | ✓ | ✓ | ✓ | **✓** | ✓ | ✓ |
| Cache | External | 10 MB | 250 MB/region | 1 GB/unit | **1 GB/unit** | 5 GB/unit | 5 GB/unit |
| Entra ID in Portal | ✗ | ✗ | ✓ | ✓ | **✓** | ✓ | ✗ |
| **DR Verdict** | NOT VIABLE | DEV ONLY | NO VNET | LEGACY | **RECOMMENDED** | NATIVE DR | NO UAE ⚠️ |

★ = Recommended for UAE North → Sweden Central DR scenario

If UAE North must remain the primary region and you demand the updated platform, **Standard v2** is your baseline. However, this means two explicitly standalone instances — aligned purely via **APIOps** and IaC. You are engineering the recovery, not toggling a magic platform feature.

---

## Designing DR for AI Services

When engineering AI into your DR posture, you must stop treating AI like a static web app. Here is how you decompose the dependencies:

---

### Azure AI Search — DR & Backup Engineering

**First principle:** Azure AI Search is explicitly *not* a primary data store. Microsoft does not provide native backup/restore or automatic cross-region replication. You own the DR story end-to-end. If your primary index corrupts and your secondary blindly mirrors it, you don't have DR — you have a fast multi-continent outage.

| Metric | Target | Notes |
|---|---|---|
| **RTO** | 15–30 min | Front Door health probe + warm standby |
| **RPO** | Near-zero | If indexer runs on both regions against shared source |
| **Min Replicas for HA** | 2 replicas | Per service SLA requires ≥2 replicas |

#### Multi-Region Architecture Pattern

Deploy two completely independent AI Search services — one in UAE North, one in Sweden Central. Both services must run the same indexer pipeline against a **geo-replicated source** (Blob Storage with GRS/GZRS, or Cosmos DB with multi-region writes). The indexer in the secondary region runs on its own schedule and is independently queryable at all times (warm standby, not cold restore).

```bash
# Deploy AI Search service in UAE North
az search service create \
  --name srch-uae-prod \
  --resource-group rg-ai-uae-prod \
  --location uaenorth \
  --sku Standard \
  --replica-count 2 \
  --partition-count 2

# Deploy identical service in Sweden Central (DR)
az search service create \
  --name srch-sweden-dr \
  --resource-group rg-ai-sweden-dr \
  --location swedencentral \
  --sku Standard \
  --replica-count 2 \
  --partition-count 2
```

#### Index Synchronisation Strategy

| Pattern | How it Works | RPO | When to Use |
|---|---|---|---|
| **Dual-indexer (recommended)** | Both regions run indexers against same GRS source. Schedule: every 5 min. | ~5 min | Production AI Search for RAG workloads |
| **Push via REST API** | App code pushes updates to both endpoints simultaneously. | <1 min | Real-time inventory, trading, live data |
| **Scheduled full re-index** | Nightly full rebuild of secondary from source. | Up to 24 hrs | Static content / large indexes, low update frequency |

> ⚠️ **Critical:** When the secondary indexer reads from the same GRS Blob Storage account, failover to the secondary storage endpoint must be pre-tested. A corrupted primary *document* will re-index into both regions. Always maintain a time-delayed snapshot of source documents (e.g., Azure Blob Lifecycle Policy archiving to Cool tier after 7 days) as your true backup layer.

#### Front Door Health Probe Configuration for Automatic Failover

```json
{
  "originGroup": "ai-search-origins",
  "healthProbe": {
    "path": "/indexes?api-version=2023-11-01",
    "protocol": "Https",
    "intervalInSeconds": 30,
    "healthProbeMethod": "HEAD"
  },
  "loadBalancingSettings": {
    "sampleSize": 4,
    "successfulSamplesRequired": 2,
    "additionalLatencyInMilliseconds": 0
  },
  "origins": [
    { "hostname": "srch-uae-prod.search.windows.net",  "priority": 1, "weight": 1000 },
    { "hostname": "srch-sweden-dr.search.windows.net", "priority": 2, "weight": 1000 }
  ]
}
```

> 💡 **Private Endpoint Note:** In a private-endpoint deployment, Front Door health probes cannot reach AI Search directly. Use a lightweight Azure Function Health Checker in each region that probes Search over private link and exposes a public `/health` endpoint.

#### Hands-On Labs & Official References — Azure AI Search DR

- 📖 [Multi-Region Solutions — Azure AI Search (MS Learn)](https://learn.microsoft.com/en-us/azure/search/search-multi-region) — Official DR guide: index sync with push/pull models, Cosmos DB change feed, Front Door failover patterns
- 💻 [Azure Search Backup & Restore Index (Azure-Samples)](https://learn.microsoft.com/en-us/samples/azure-samples/azure-search-dotnet-utilities/azure-search-backup-restore-index/) — .NET/Python code sample: serialize index to JSON, restore across services
- 💻 [azure-search-multiple-regions (GitHub)](https://github.com/Azure-Samples/azure-search-multiple-regions) — Complete BCDR reference: multi-region deployment with Front Door + Cosmos DB change feed

---

### Azure Document Intelligence — DR & Backup Engineering

**Architecture reality:** Azure Document Intelligence is a *regional* resource. There is no built-in cross-region failover toggle. DR requires deploying at minimum two separate resources — one per region — and using the **Model Copy API** to replicate custom models and classifiers. Out-of-the-box prebuilt models (Invoice, Receipt, Layout) are available in all regions and need no copy.

| Metric | Target | Notes |
|---|---|---|
| **RTO** | 10–20 min | Front Door failover + warm model copy |
| **RPO** | ~24 hrs | Daily scheduled model copy pipeline |
| **Copy API Tier** | S0 minimum | Free tier does not support Copy API |

#### Model Copy API — Step-by-Step Runbook

The Copy API is a two-phase operation: **authorize on target**, then **initiate copy from source**. Both resources must use the same pricing tier (S0). The copy is asynchronous — poll the operation URL until status is `succeeded`.

```bash
# Step 1: Authorize copy on TARGET (Sweden Central)
TARGET_ENDPOINT="https://docintel-sweden-dr.cognitiveservices.azure.com"
TARGET_KEY="<sweden-dr-api-key>"
MODEL_ID="my-custom-invoice-classifier"

AUTHORIZATION=$(curl -s -X POST \
  "${TARGET_ENDPOINT}/documentintelligence/documentModels/${MODEL_ID}:authorizeCopy?api-version=2024-02-29-preview" \
  -H "Ocp-Apim-Subscription-Key: ${TARGET_KEY}" \
  -H "Content-Type: application/json" \
  -d '{"modelId": "'"${MODEL_ID}"'"}')

# Step 2: Initiate copy FROM SOURCE (UAE North)
SOURCE_ENDPOINT="https://docintel-uae-prod.cognitiveservices.azure.com"
SOURCE_KEY="<uae-prod-api-key>"

OPERATION_URL=$(curl -s -D - -o /dev/null -X POST \
  "${SOURCE_ENDPOINT}/documentintelligence/documentModels/${MODEL_ID}:copyTo?api-version=2024-02-29-preview" \
  -H "Ocp-Apim-Subscription-Key: ${SOURCE_KEY}" \
  -H "Content-Type: application/json" \
  -d "${AUTHORIZATION}" | grep -i 'operation-location' | tr -d '\r' | cut -d' ' -f2)

# Step 3: Poll until succeeded
while true; do
  STATUS=$(curl -s "${OPERATION_URL}" -H "Ocp-Apim-Subscription-Key: ${SOURCE_KEY}" \
    | python3 -c "import sys,json; print(json.load(sys.stdin)['status'])")
  echo "Status: ${STATUS}"
  [[ "${STATUS}" == "succeeded" || "${STATUS}" == "failed" ]] && break
  sleep 10
done
```

#### Automated Daily Model Sync Pipeline

Wrap the above script into an **Azure Logic App** or **Azure DevOps pipeline** scheduled daily. The pipeline should:

1. List all custom models from UAE North using `GET /documentintelligence/documentModels?api-version=2024-02-29-preview`
2. For each model, check if Sweden Central version's `lastUpdatedDateTime` is older than source — only copy if stale
3. Send a Teams/email alert on copy failure so engineers can manually intervene before the next potential DR event

> ⚠️ **Zero-Trust Secret Management:** Each regional Document Intelligence resource must have its own **separate Key Vault** in the same region. Cross-region Key Vault lookups during a DR event create latency and availability dependency chains. APIM Named Values must point to the local regional KV reference — not a shared cross-region KV.

#### Hands-On Labs & Official References — Azure Document Intelligence DR

- 📖 [Disaster Recovery Guidance — Document Intelligence (MS Learn)](https://learn.microsoft.com/en-us/azure/ai-services/document-intelligence/how-to-guides/disaster-recovery?view=doc-intel-4.0.0) — Official Copy API walkthrough: authorize → copy → poll
- 💻 [document-intelligence-code-samples (Azure-Samples)](https://github.com/Azure-Samples/document-intelligence-code-samples) — Runnable SDK samples in Python, C#, Java, and JavaScript

---

### Azure AI Foundry & Model Endpoints — DR & Backup Engineering

**The hard constraint that kills most DR plans:** Azure AI Foundry provides *no automatic failover*. PTU (Provisioned Throughput Units) cannot be auto-spun in a secondary region under duress. You must pre-allocate PTU capacity in Sweden Central *before* you need it. Assuming you can spin up PTU during a sev-1 at 3 AM is a fast track to an executive-level outage post-mortem.

| Metric | Target | Notes |
|---|---|---|
| **RTO** | 30–60 min | Manual operator-triggered cutover (no auto) |
| **RPO** | Agent state: ~1 hr | Cosmos DB backup interval dependent |
| **Model Deployments** | Static config | IaC-deployed, no copy API — redeploy from Bicep |

#### PTU Pre-Allocation Strategy

| Pattern | UAE North (Primary) | Sweden Central (DR) | Cost | RTO |
|---|---|---|---|---|
| **Active-Active PTU** | Full PTU (e.g., 100 PTU) | Full PTU (100 PTU) | 2× PTU cost always | ~5 min (Front Door reroute) |
| **Workload + Enterprise Pool (recommended)** | Workload PTU (dedicated, 100 PTU) | Enterprise Data Zone PTU pool (shared) | ~40–60% saving on DR region | 15–20 min (pool allocation) |
| **PTU Primary + PAYG DR** | PTU (100 PTU) | Standard (PAYG) — no pre-purchase | Lowest cost | 45–90 min + throttle risk |

#### Agent State Backup — Cosmos DB Configuration

Azure AI Foundry Agent Service stores conversation threads, tool call history, and agent configuration in a **customer-provisioned Azure Cosmos DB** account. This is the only stateful component of the AI Foundry stack. If you skip this, your agents lose all session context on failover.

```bash
# Configure Cosmos DB for AI Foundry Agent Service with multi-region writes
az cosmosdb create \
  --name cosmos-agents-prod \
  --resource-group rg-ai-uae-prod \
  --locations regionName="UAE North" failoverPriority=0 isZoneRedundant=true \
  --locations regionName="Sweden Central" failoverPriority=1 isZoneRedundant=false \
  --enable-multiple-write-locations true \
  --default-consistency-level Session \
  --backup-policy-type Continuous \
  --continuous-mode-backup-interval 240

# Link Cosmos DB to AI Foundry Project during hub creation
az ml workspace create \
  --name ai-foundry-uae-hub \
  --resource-group rg-ai-uae-prod \
  --location uaenorth \
  --kind hub \
  --cosmos-db-id "/subscriptions/<sub-id>/resourceGroups/rg-ai-uae-prod/providers/Microsoft.DocumentDB/databaseAccounts/cosmos-agents-prod"
```

#### Model Deployment Parity via Bicep

Model deployments in AI Foundry are configuration objects — there is no "copy API." The only safe DR approach is Infrastructure as Code with identical deployment manifests for both regions:

```bicep
// Bicep: Deploy identical GPT-4o deployment in both regions
param location string
param hubName string

resource gpt4oDeployment 'Microsoft.CognitiveServices/accounts/deployments@2023-10-01-preview' = {
  name: '${hubName}/gpt-4o-deployment'
  properties: {
    model: {
      format: 'OpenAI'
      name: 'gpt-4o'
      version: '2024-05-13'
    }
    scaleSettings: {
      scaleType: 'Standard'  // Switch to 'ProvisionedManaged' for PTU
      capacity: 10
    }
  }
}

// Deploy to UAE:    az deployment group create --parameters location=uaenorth    hubName=ai-foundry-uae-hub
// Deploy to Sweden: az deployment group create --parameters location=swedencentral hubName=ai-foundry-sweden-hub
```

#### AI Foundry DR Failover Runbook (6 Steps)

1. **Detect:** Azure Monitor alert fires on `SuccessRate < 95%` on UAE North AI Foundry endpoint for >5 minutes
2. **Validate:** Run synthetic test against Sweden Central AI Foundry endpoint — confirm model responds correctly
3. **Switch:** Update Front Door origin weights (UAE=0, Sweden=1000) or disable UAE origin entirely
4. **APIM:** Verify Named Values (`ai-foundry-endpoint`) point to Sweden Central — update via APIOps if not already parameterized
5. **Cosmos DB:** Trigger manual failover if UAE North Cosmos region is also unavailable:
   ```bash
   az cosmosdb failover-priority-change \
     --name cosmos-agents-prod \
     --failover-policies "Sweden Central=0" "UAE North=1"
   ```
6. **Notify:** Alert on-call + stakeholders, open sev-1 bridge

#### Hands-On Labs & Official References — Azure AI Foundry DR

- 📖 [Customer-Enabled DR for AI Hub Projects (MS Learn)](https://learn.microsoft.com/en-us/azure/ai-foundry/how-to/disaster-recovery) — Official BCDR guide: regional failure handling, storage redundancy, multi-region hub deployment
- 📖 [BCDR for Azure OpenAI in AI Foundry (MS Learn)](https://learn.microsoft.com/en-us/azure/ai-foundry/openai/how-to/business-continuity-disaster-recovery) — Multi-region failover and resource redundancy for Azure OpenAI model deployments
- 📖 [Agent Service Disaster Recovery (MS Learn)](https://learn.microsoft.com/en-us/azure/ai-foundry/how-to/agent-service-disaster-recovery?view=foundry-classic) — Agent Service-specific DR: Cosmos DB for agent state persistence, regional recovery procedures

---

### Azure API Management — Backup, Restore & DR Engineering

**APIM DR architecture decision:** Standard v2 in UAE North + Standard v2 in Sweden Central means two completely *independent* instances. Microsoft provides a native Backup/Restore REST API to export and import service configuration. Backup captures configuration, not traffic state. Your DR posture is a combination of regular backups + APIOps pipeline for config parity + Front Door for traffic routing.

| Metric | Target | Notes |
|---|---|---|
| **RTO** | 5–15 min | Front Door reroute (warm standby) |
| **RPO** | <1 hr | Hourly backup + APIOps pipeline parity |
| **Backup Supported Tiers** | Dev, Basic, Std, Premium | Not supported on Consumption tier |

#### APIM Backup REST API — Automated Hourly Schedule

Always backup to a **geo-redundant storage account** (GRS or GZRS) so the backup blob is available even if the primary region is down.

```bash
SUBSCRIPTION_ID="<your-subscription-id>"
RESOURCE_GROUP="rg-apim-uae-prod"
APIM_NAME="apim-uae-prod"
STORAGE_ACCOUNT="stbackupapim"   # GRS storage account
STORAGE_CONTAINER="apim-backups"
BACKUP_NAME="apim-uae-$(date +%Y%m%d-%H%M)"
STORAGE_KEY=$(az storage account keys list --account-name ${STORAGE_ACCOUNT} --query '[0].value' -o tsv)

az rest --method post \
  --url "https://management.azure.com/subscriptions/${SUBSCRIPTION_ID}/resourceGroups/${RESOURCE_GROUP}/providers/Microsoft.ApiManagement/service/${APIM_NAME}/backup?api-version=2022-08-01" \
  --body "{
    \"storageAccount\": \"${STORAGE_ACCOUNT}\",
    \"containerName\": \"${STORAGE_CONTAINER}\",
    \"backupName\": \"${BACKUP_NAME}\",
    \"accessType\": \"StorageAccessKey\",
    \"accessKey\": \"${STORAGE_KEY}\"
  }"
```

#### APIM Restore to DR Instance

```bash
DR_RESOURCE_GROUP="rg-apim-sweden-dr"
DR_APIM_NAME="apim-sweden-dr"
BACKUP_NAME="apim-uae-20260418-0300"

az rest --method post \
  --url "https://management.azure.com/subscriptions/${SUBSCRIPTION_ID}/resourceGroups/${DR_RESOURCE_GROUP}/providers/Microsoft.ApiManagement/service/${DR_APIM_NAME}/restore?api-version=2022-08-01" \
  --body "{
    \"storageAccount\": \"${STORAGE_ACCOUNT}\",
    \"containerName\": \"${STORAGE_CONTAINER}\",
    \"backupName\": \"${BACKUP_NAME}\",
    \"accessType\": \"StorageAccessKey\",
    \"accessKey\": \"${STORAGE_KEY}\"
  }"

# Always run APIOps publisher AFTER restore to re-apply environment-specific Named Values
```

> ⚠️ **What APIM Backup Does NOT Include:**
> - Custom gateway certificates — store in Key Vault and re-bind post-restore
> - Named Values that reference Key Vault secrets — KV references need separate regional KV setup
> - Analytics data and logs — these live in Azure Monitor / Application Insights
> - Identity provider configuration secrets — re-configure OAuth app secrets post-restore

#### APIOps Pipeline for Continuous Config Parity

Backup + restore is a recovery tool, not a sync tool. For continuous parity, configure an APIOps extractor/publisher pipeline that runs on every merge to `main`:

```yaml
# azure-pipelines-apiops.yml
trigger:
  branches:
    include: [ main ]

stages:
- stage: ExtractUAE
  jobs:
  - job: Extract
    steps:
    - task: AzureCLI@2
      displayName: 'Extract APIM config from UAE North'
      inputs:
        scriptType: bash
        scriptLocation: inlineScript
        inlineScript: |
          ./extractor/run.sh \
            --apimServiceName apim-uae-prod \
            --resourceGroupName rg-apim-uae-prod \
            --apiSpecificationFormat OpenApiJson \
            --outputFolder $(Build.ArtifactStagingDirectory)/apim-config

- stage: PublishSweden
  dependsOn: ExtractUAE
  condition: succeeded()
  jobs:
  - job: Publish
    steps:
    - task: AzureCLI@2
      displayName: 'Publish extracted config to Sweden Central'
      inputs:
        scriptType: bash
        scriptLocation: inlineScript
        inlineScript: |
          ./publisher/run.sh \
            --apimServiceName apim-sweden-dr \
            --resourceGroupName rg-apim-sweden-dr \
            --configFile $(Build.ArtifactStagingDirectory)/apim-config/configuration.yaml \
            --overrideNamedValues "ai-foundry-endpoint=$(SWEDEN_AI_ENDPOINT)" \
                                  "ai-search-endpoint=$(SWEDEN_SEARCH_ENDPOINT)"
```

> 💡 **Key insight:** The `--overrideNamedValues` flag allows the same extracted APIM configuration to deploy to two different regions pointing to region-specific backend endpoints. Without this, the Sweden DR APIM will silently point all its policies to UAE North backends — a failure that only reveals itself during an actual DR event.

#### Hands-On Labs & Official References — Azure APIM Backup & DR

- 📖 [APIM Backup & Restore for DR (MS Learn)](https://learn.microsoft.com/en-us/azure/api-management/api-management-howto-disaster-recovery-backup-restore) — Official backup/restore REST API reference with PowerShell and ARM examples
- 💻 [Azure APIOps Toolkit (GitHub — Azure/apiops)](https://github.com/Azure/apiops) — Official APIOps extractor + publisher toolkit for multi-region APIM config parity
- 📐 [Automated API Deployments via APIOps (Azure Architecture Center)](https://learn.microsoft.com/en-us/azure/architecture/example-scenario/devops/automated-api-deployments-apiops) — APIOps CI/CD pipeline Dev → QA → Prod with environment-specific Named Value overrides

---

## Enterprise Landing Zone Engineering

We do not dump these systems into disparate resource groups. We design them into an aligned Azure Landing Zone utilizing a strict hub-and-spoke pattern.

**Figure 1:** Complete Zero-Trust DR Architecture across UAE North and Sweden Central  
*(See: `azure_ai_dr_landing_zone.webp` in this folder)*

### The Architectural Verification Sequence

- [ ] **Private Endpoints:** Ensure granular isolation and explicit routing per region without public ingress.
- [ ] **Central DNS Integrity:** Resolve Private Link DNS explicitly avoiding Split-Brain failures during cutovers.
- [ ] **WAF Decoupling:** Use Application Gateway with WAF ahead of APIM. WAF controls edge protection; APIM manages policy mediation.
- [ ] **Runbook Orchestration:** Script the entire failover flow. Do not rely on manual operators during a sev-1.

---

## APIM DR Alternatives at a Glance

| Tier | Native Platform Mechanism | Architectural Burden | Recommendation |
|---|---|---|---|
| **Standard v2** | Modern scaling across UAE and Sweden independently. | Total customer-owned DR routing, config parity, failover runbooks via APIOps. | ✅ Recommended if UAE primary & v2 alignment are strict requirements. |
| **Premium classic** | Built-in multi-region gateway propagation. | Testing governance, managing complex rollbacks globally. | ✅ Recommended if "native multi-region" APIM drives board approval. |
| **Premium v2** | Availability Zones in selected geographies. | Massive constraint: Not deployable in UAE North today. | ❌ Reject outright for this exact scenario. |

---

## Engineer's Runbook: Deploying the DR Pattern

### 1. Decoupling Infrastructure from API Governance (APIOps)

Because Standard v2 APIM instances are entirely independent, manually recreating APIs in Sweden Central leads to configuration drift and inevitable outage during failover.

**The Rule:** Deploy the APIM infrastructure shells via parameterized Bicep/Terraform (`main.bicep` with `var.uae` and `var.sweden`). Then establish an [Azure APIOps](https://github.com/Azure/apiops) pipeline. The APIOps extractor pulls API designs, named values, and policies from UAE North and the publisher deploys them immutably to Sweden Central.

### 2. Azure Front Door Priority Origin Configuration

You cannot use a simple Active/Passive traffic manager. Configure Azure Front Door with strict origin priorities to ensure Sweden Central only receives health-probe traffic until UAE North drops below acceptable health thresholds.

```bicep
// Bicep: Azure Front Door Origin Routing Logic
resource originGroup 'Microsoft.Cdn/profiles/originGroups@2023-05-01' = {
  name: 'dr-origin-group'
  parent: frontDoorProfile
  properties: {
    loadBalancingSettings: {
      sampleSize: 4
      successfulSamplesRequired: 3
    }
    healthProbeSettings: {
      probePath: '/status-0123456789abcdef' // Secure APIM health probe URL
      probeProtocol: 'Https'
      probeIntervalInSeconds: 60
    }
  }
}

// UAE North - Active (Priority 1)
resource uaeOrigin 'Microsoft.Cdn/profiles/originGroups/origins@2023-05-01' = {
  name: 'uae-appgw-origin'
  parent: originGroup
  properties: {
    hostName: uaeAppGatewayFQDN
    priority: 1
    weight: 1000
  }
}

// Sweden Central - Standby (Priority 2)
resource swedenOrigin 'Microsoft.Cdn/profiles/originGroups/origins@2023-05-01' = {
  name: 'sweden-appgw-origin'
  parent: originGroup
  properties: {
    hostName: swedenAppGatewayFQDN
    priority: 2    // Activated on Priority 1 failure
    weight: 1000
  }
}
```

### 3. Private Endpoint & Hub DNS Wiring

A fatal multi-region mistake is failing to isolate DNS resolution. If APIM in Sweden Central attempts to resolve `my-ai-search.privatelink.search.windows.net` and it resolves to the dead UAE North private IP, the failover collapses.

- **The Fix:** Do not link the global Hub VNet Private DNS Zone statically. Use **Azure Private DNS Virtual Network Links** localized per region, or leverage Azure Firewall DNS proxies as forwarders.
- Configure APIM networking to explicitly point its custom DNS setting to the local regional subset (or local Azure Firewall IP acting as DNS proxy) so that the same AI Search `privatelink` URL resolves to the local Sweden Central endpoint.

### 4. Operator Cut-over Checklist

**Figure 2:** Sequence of required manual and automated validation gates during cutover  
*(See: `azure_dr_failover_runbook.webp` in this folder)*

Automated DR failovers for AI systems are structurally dangerous. Document a precise operator trigger:

1. **Confirm Priority Shift:** Validate Front Door has automatically evicted Priority 1 and traffic is flowing to Priority 2 matching the telemetry dashboards.
2. **Validate Data Freshness:** Verify Sweden Central AI Search Index synchronization is within the RPO acceptable timeframe (< 5 minutes stale) before unlocking full user write capabilities.
3. **Re-test Grounding:** Execute an explicit end-to-end synthetic API test hitting the Sweden Central APIM to ensure the RAG model successfully queries the DR Search Vector Index before publicly declaring the failover sequence successful.

---

## Front Door + APIM Origin Lockdown Pattern

A critical hardening step most architects skip: ensuring that APIM instances **only accept traffic routed through Azure Front Door**, not direct public internet hits.

> **The Nightclub Bouncer Analogy:** Think of Azure Front Door as the only legitimate entrance to your nightclub (APIM). The NSG is the velvet rope that blocks anyone who tries to sneak in through the kitchen door. The global APIM policy is the bouncer inside who checks every guest's VIP wristband (`X-Azure-FDID` header).

### Step 1: NSG — Block All Non-Front-Door Ingress

```bicep
resource nsg 'Microsoft.Network/networkSecurityGroups@2023-05-01' = {
  name: 'nsg-apim-${regionSuffix}'
  location: location
  properties: {
    securityRules: [
      {
        name: 'AllowFrontDoorInbound'
        properties: {
          priority: 100
          direction: 'Inbound'
          access: 'Allow'
          protocol: 'Tcp'
          sourcePortRange: '*'
          destinationPortRange: '443'
          sourceAddressPrefix: 'AzureFrontDoor.Backend'
          destinationAddressPrefix: 'VirtualNetwork'
        }
      }
      {
        name: 'AllowAPIMManagement'
        properties: {
          priority: 110
          direction: 'Inbound'
          access: 'Allow'
          protocol: 'Tcp'
          sourcePortRange: '*'
          destinationPortRange: '3443'
          sourceAddressPrefix: 'ApiManagement'
          destinationAddressPrefix: 'VirtualNetwork'
        }
      }
      {
        name: 'DenyAllOtherInbound'
        properties: {
          priority: 4096
          direction: 'Inbound'
          access: 'Deny'
          protocol: '*'
          sourcePortRange: '*'
          destinationPortRange: '*'
          sourceAddressPrefix: '*'
          destinationAddressPrefix: '*'
        }
      }
    ]
  }
}
```

### Step 2: Global APIM Policy — Validate the `X-Azure-FDID` Header

NSG rules alone are necessary but **not sufficient**. The `AzureFrontDoor.Backend` service tag permits traffic from *any* Front Door instance globally. Validate the `X-Azure-FDID` header to ensure requests come from *your specific* Front Door profile:

```xml
<!-- Global APIM Policy: Validate Front Door ID -->
<policies>
  <inbound>
    <base />
    <check-header name="X-Azure-FDID"
                  failed-check-httpcode="403"
                  failed-check-error-message="Invalid Front Door ID"
                  ignore-case="false">
      <value>{{front-door-id}}</value>
    </check-header>
  </inbound>
</policies>
```

> ⚠️ **DR-Critical Note:** Store the Front Door ID as a **Named Value** in each regional APIM instance. Your APIOps pipeline must propagate this value identically to *both* UAE North and Sweden Central instances. If the Sweden Central APIM has a stale or missing Front Door ID, **every request will return 403 during failover** — defeating the entire DR exercise.

### Step 3: Apply to Both Regions via APIOps

This lockdown must be **identical in both regions**. The APIOps pipeline must include:

- **Named Values:** Specifically `front-door-id` — extracted from UAE North and published to Sweden Central.
- **Global Policy XML:** The `check-header` policy must live in the all-APIs policy scope, not per-API.
- **NSG Terraform/Bicep modules:** Parameterized per region (`var.uae`, `var.sweden`).

> Without this pattern, a direct-to-APIM attack during a region failover can bypass Front Door's WAF, DDoS protection, and health-probe routing entirely. The NSG + header validation combination creates **defense-in-depth that survives region cutovers**.

---

## The Traps to Avoid

Enterprise deployments stall at the design phase due to predictable mistakes:

- **Confusing HA with DR.** High Availability = intra-region AZ distribution. Disaster Recovery = cross-region localized isolation. They are not the same thing.
- **Expecting AI Foundry to auto-scale during a planetary-scale event.** Without distinct RTO/RPO models and pre-allocated PTU, this is an architectural gamble you will lose.
- **Passive DNS assumption.** If APIM in your DR region resolves private link hostnames to the primary region's dead private IPs, your failover collapses silently.
- **Shared Key Vault across regions.** A single KV in UAE North as a dependency during a UAE North outage is a circular failure dependency.
- **Running APIOps extract/publish only on initial setup.** Every API change in UAE North must be immediately published to Sweden Central or you accumulate silent drift.

### Final Stance

A cross-geography DR pattern for AI and API workloads is inherently a **customer-engineered resilience pattern, not a product feature bundle**. If you are going this route, commit to:

- Standard v2 with twin regional instances
- Separate regional AI model commitments (PTU pre-allocated)
- A DNS governance strategy that actually survives cutover night

That is not the lowest effort design, but it is the one you can confidently stand behind when the dashboard turns red.

---

## References & Further Reading

### Azure AI Search
- [Multi-Region Solutions — Azure AI Search](https://learn.microsoft.com/en-us/azure/search/search-multi-region)
- [Azure Search Backup & Restore Index (Azure-Samples)](https://learn.microsoft.com/en-us/samples/azure-samples/azure-search-dotnet-utilities/azure-search-backup-restore-index/)
- [azure-search-multiple-regions (GitHub)](https://github.com/Azure-Samples/azure-search-multiple-regions)

### Azure Document Intelligence
- [Disaster Recovery Guidance — Document Intelligence](https://learn.microsoft.com/en-us/azure/ai-services/document-intelligence/how-to-guides/disaster-recovery?view=doc-intel-4.0.0)
- [document-intelligence-code-samples (Azure-Samples)](https://github.com/Azure-Samples/document-intelligence-code-samples)

### Azure AI Foundry
- [Customer-Enabled DR for AI Hub Projects](https://learn.microsoft.com/en-us/azure/ai-foundry/how-to/disaster-recovery)
- [BCDR for Azure OpenAI in AI Foundry](https://learn.microsoft.com/en-us/azure/ai-foundry/openai/how-to/business-continuity-disaster-recovery)
- [Agent Service Disaster Recovery](https://learn.microsoft.com/en-us/azure/ai-foundry/how-to/agent-service-disaster-recovery?view=foundry-classic)

### Azure API Management
- [APIM Backup & Restore for DR](https://learn.microsoft.com/en-us/azure/api-management/api-management-howto-disaster-recovery-backup-restore)
- [Azure APIOps Toolkit (GitHub)](https://github.com/Azure/apiops)
- [Automated API Deployments via APIOps — Azure Architecture Center](https://learn.microsoft.com/en-us/azure/architecture/example-scenario/devops/automated-api-deployments-apiops)

### General
- [Azure Quickstart: Front Door Standard/Premium with API Management](https://learn.microsoft.com/en-us/samples/azure/azure-quickstart-templates/front-door-standard-premium-api-management-external/) — NSG lockdown + `X-Azure-FDID` header validation pattern
- [APIM with VNet — External Mode](https://learn.microsoft.com/en-us/azure/api-management/api-management-using-with-vnet) — Required NSG rules for APIM management traffic
- [Full Bicep/ARM Source Code (GitHub)](https://github.com/azure/azure-quickstart-templates/tree/master/quickstarts/microsoft.cdn/front-door-standard-premium-api-management-external) — Deploy the Front Door + APIM lockdown template directly

---

*Written by Upendra Kumar — Cloud Solutions Architect specializing in Azure AI, APIM, and enterprise-scale resilience patterns.*  
*Portfolio: https://portfolio.upendrakumar.com*

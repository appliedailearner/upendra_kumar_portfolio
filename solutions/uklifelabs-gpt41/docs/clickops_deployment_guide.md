# ClickOps Implementation Guide: AI Fortress Deployment

**Purpose**: Step-by-step Azure Portal instructions for deploying the AI Fortress architecture without Terraform.

---

## Prerequisites

- Azure subscription with Owner/Contributor access
- 50 PTU quota approved in UK South
- Azure CLI installed (for verification steps)

---

## Phase 1: Hub Subscription Setup

### 1.1 Create Hub Resource Group
1. Navigate to **Resource Groups** → **Create**
2. **Subscription**: Select "Shared Services"
3. **Resource Group**: `rg-shared-hub-uks`
4. **Region**: UK South
5. Click **Review + Create**

### 1.2 Deploy Hub VNet
1. Navigate to **Virtual Networks** → **Create**
2. **Name**: `vnet-shared-uks-hub`
3. **Address Space**: `10.100.0.0/16`
4. **Subnets**:
   - `snet-firewall`: `10.100.1.0/26`
   - `snet-shared-pe`: `10.100.2.0/24`
   - `snet-dns-resolver`: `10.100.3.0/28`

### 1.3 Deploy Azure Firewall Premium
1. Navigate to **Firewalls** → **Create**
2. **Name**: `afw-shared-hub-premium`
3. **Tier**: Premium
4. **VNet**: `vnet-shared-hub-uks`
5. **Subnet**: `snet-firewall`
6. **Enable IDPS**: Alert and Deny mode
7. **Enable TLS Inspection**: Yes

### 1.4 Deploy Private DNS Resolver
1. Navigate to **Private DNS Resolvers** → **Create**
2. **Name**: `pdns-resolver-hub`
3. **VNet**: `vnet-shared-hub-uks`
4. **Inbound Endpoint Subnet**: `snet-dns-resolver`

---

## Phase 2: Prod Spoke Setup

### 2.1 Create Prod Resource Group
1. Navigate to **Resource Groups** → **Create**
2. **Subscription**: Select "Production"
3. **Resource Group**: `rg-prod-spoke-uks`
4. **Region**: UK South

### 2.2 Deploy Spoke VNet
1. Navigate to **Virtual Networks** → **Create**
2. **Name**: `vnet-prod-uks-spoke`
3. **Address Space**: `10.1.0.0/16`
4. **Subnets**:
   - `snet-aks-nodes`: `10.1.1.0/24`
   - `snet-appgw`: `10.1.2.0/24`
   - `snet-ai-be`: `10.1.3.0/24`
   - `snet-redis`: `10.1.4.0/28`

### 2.3 Create VNet Peering
1. Navigate to Hub VNet → **Peerings** → **Add**
2. **Peering Name**: `hub-to-prod-spoke`
3. **Remote VNet**: `vnet-prod-uks-spoke`
4. **Allow Gateway Transit**: Yes (on Hub side)
5. **Use Remote Gateway**: Yes (on Spoke side)

---

## Phase 3: Azure Redis Cache

### 3.1 Deploy Redis Premium
1. Navigate to **Azure Cache for Redis** → **Create**
2. **Name**: `redis-prod-uks-cache`
3. **Pricing Tier**: Premium P1 (6 GB)
4. **Location**: UK South
5. **VNet**: `vnet-prod-uks-spoke`
6. **Subnet**: `snet-redis`
7. **TLS Version**: 1.2 (minimum)
8. **Maxmemory Policy**: allkeys-lru

### 3.2 Create Private Endpoint for Redis
1. Navigate to Redis → **Private Endpoint Connections** → **Add**
2. **Name**: `pe-redis-prod`
3. **VNet**: `vnet-shared-hub-uks`
4. **Subnet**: `snet-shared-pe`
5. **Integrate with Private DNS**: Yes
6. **DNS Zone**: `privatelink.redis.cache.windows.net`

---

## Phase 4: Azure OpenAI with PTU Split

### 4.1 Create OpenAI Account
1. Navigate to **Azure OpenAI** → **Create**
2. **Name**: `oai-prod-uks`
3. **Pricing Tier**: S0
4. **Region**: UK South
5. **Network**: Disable public access
6. **Custom Subdomain**: `ukl-openai-prod`

### 4.2 Create Production Deployment (30 PTU)
1. Navigate to OpenAI → **Model Deployments** → **Create**
2. **Deployment Name**: `gpt4-prod-deployment`
3. **Model**: GPT-4 Turbo (2024-04-09)
4. **Deployment Type**: Provisioned-Managed
5. **PTU Capacity**: 30

### 4.3 Create Test Deployment (10 PTU)
1. Repeat Step 4.2 with:
   - **Deployment Name**: `gpt4-test-deployment`
   - **PTU Capacity**: 10

### 4.4 Create Dev Deployment (10 PTU)
1. Repeat Step 4.2 with:
   - **Deployment Name**: `gpt4-dev-deployment`
   - **PTU Capacity**: 10

### 4.5 Create Private Endpoint for OpenAI
1. Navigate to OpenAI → **Networking** → **Private Endpoint**
2. **Name**: `pe-openai-prod`
3. **VNet**: `vnet-shared-hub-uks`
4. **Subnet**: `snet-shared-pe`
5. **DNS Zone**: `privatelink.openai.azure.com`

---

## Phase 5: APIM Configuration

### 5.1 Deploy APIM (Internal Mode)
1. Navigate to **API Management** → **Create**
2. **Name**: `apim-prod-internal`
3. **Pricing Tier**: Developer (for testing) or Premium (for production)
4. **VNet**: `vnet-prod-uks-spoke`
5. **Subnet**: `snet-ai-be`
6. **VNet Type**: Internal

### 5.2 Configure Redis Cache Connection
1. Navigate to APIM → **External Cache**
2. **Use from**: Custom
3. **Connection String**: Retrieve from Redis → **Access Keys**
4. **Save**

### 5.3 Add Caching Policy
1. Navigate to APIM → **APIs** → **Add API** → **OpenAI**
2. **Inbound Processing** → **Add Policy** → **Cache Lookup**:
   ```xml
   <cache-lookup vary-by-developer="false" caching-type="external">
       <vary-by-query-parameter>prompt</vary-by-query-parameter>
   </cache-lookup>
   ```
3. **Outbound Processing** → **Add Policy** → **Cache Store**:
   ```xml
   <cache-store duration="3600" caching-type="external" />
   ```

### 5.4 Add Environment-Based Routing
1. **Inbound Processing** → **Set Backend Service**:
   ```xml
   <choose>
       <when condition="@(context.Request.Headers.GetValueOrDefault("X-Environment","prod") == "prod")">
           <set-backend-service base-url="https://ukl-openai-prod.openai.azure.com/openai/deployments/gpt4-prod-deployment" />
       </when>
       <when condition="@(context.Request.Headers.GetValueOrDefault("X-Environment","") == "test")">
           <set-backend-service base-url="https://ukl-openai-prod.openai.azure.com/openai/deployments/gpt4-test-deployment" />
       </when>
       <when condition="@(context.Request.Headers.GetValueOrDefault("X-Environment","") == "dev")">
           <set-backend-service base-url="https://ukl-openai-prod.openai.azure.com/openai/deployments/gpt4-dev-deployment" />
       </when>
   </choose>
   ```

---

## Phase 6: Azure Policy (MCSB v2)

### 6.1 Assign MCSB v2 Initiative
1. Navigate to **Policy** → **Definitions**
2. Search for "Microsoft Cloud Security Benchmark v2"
3. **Assign** to Subscription
4. **Assignment Name**: `mcsb-v2-compliance`
5. **Effect**: AuditIfNotExists
6. **Create Managed Identity**: Yes
7. **Assign**

### 6.2 Monitor Compliance
1. Navigate to **Policy** → **Compliance**
2. Filter by "MCSB v2"
3. Review non-compliant resources
4. Create remediation tasks as needed

---

## Phase 7: Verification

### 7.1 Test DNS Resolution
```bash
az aks command invoke \
  --resource-group rg-prod-spoke-uks \
  --name aks-prod-uks \
  --command "nslookup ukl-openai-prod.privatelink.openai.azure.com"
```
**Expected**: Private IP (10.100.x.x)

### 7.2 Test Redis Connection
```bash
redis-cli -h redis-prod-uks-cache.redis.cache.windows.net \
  -p 6380 \
  -a <access-key> \
  --tls PING
```
**Expected**: PONG

### 7.3 Test Semantic Caching
1. Send first request to APIM with prompt "What is Azure?"
2. Note response time (e.g., 2000ms)
3. Send identical request
4. **Expected**: Response time <50ms (cache hit)

---

## Troubleshooting

**Issue**: DNS not resolving to private IP  
**Fix**: Ensure VNet is linked to Private DNS Zone

**Issue**: Redis connection timeout  
**Fix**: Check NSG rules allow port 6380 from APIM subnet

**Issue**: PTU deployment fails  
**Fix**: Verify quota in Azure Portal → Subscriptions → Quotas

---

## Cost Estimate

| Resource | Monthly Cost (GBP) |
|----------|-------------------|
| Azure Firewall Premium | £1,200 |
| Redis Cache Premium P1 | £250 |
| OpenAI 50 PTU | £15,500 |
| APIM Premium | £1,800 |
| **Total** | **£18,750** |

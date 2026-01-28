# Architecture Diagram Regeneration Prompts

**Purpose**: Comprehensive prompts to regenerate all architecture diagrams with Redis Cache, PTU split, and MCSB v2 compliance.

**Style Guide**: Microsoft Azure Architecture Diagram Style
- Clean, professional, corporate aesthetic
- Light background (white or very light blue #F5F9FF)
- Azure blue accent color (#0078D4)
- Clear component labels
- Logical flow from left to right or top to bottom
- Icons should be simple, recognizable Azure service icons

---

## Diagram 1: Complete Solution Overview

**Filename**: `uklifelabs_solution_overview_corporate.png`

**Prompt**:
```
Create a Microsoft Azure architecture diagram showing the complete AI Fortress solution with the following components:

STYLE:
- Clean, light, professional Microsoft corporate style
- White/light blue background (#F5F9FF)
- Azure blue accents (#0078D4)
- Clear labels, modern sans-serif font
- Logical left-to-right flow

LAYOUT (4 Subscription Columns):

Column 1 - SHARED HUB SUBSCRIPTION:
- Azure Front Door Premium (global icon at top)
- Hub VNet (10.100.0.0/16) containing:
  - Azure Firewall Premium with IDPS
  - Private Endpoint subnet (centralized)
  - Private DNS Resolver
- Label: "Shared Services Hub"

Column 2 - PRODUCTION SPOKE:
- Prod VNet (10.1.0.0/16) containing:
  - Application Gateway (AGIC)
  - AKS Private Cluster (with pods)
  - APIM Internal (AI Gateway)
  - Azure Redis Cache Premium (NEW - highlight with subtle glow)
  - Private Endpoints for OpenAI, SQL, Storage
- VNet Peering arrow to Hub
- Label: "Production Spoke (UK South)"

Column 3 - OPENAI & DATA SERVICES:
- Azure OpenAI with 3 deployments (show as stacked boxes):
  - "Prod: 30 PTU" (largest box)
  - "Test: 10 PTU" (medium box)
  - "Dev: 10 PTU" (medium box)
- Azure SQL Database
- Azure Storage (GRS)
- Azure Key Vault
- Label: "AI & Data Layer"

Column 4 - DR REGION:
- UK West VNet (standby)
- Azure Container Registry (geo-replicated)
- Standby AKS
- Recovery Services Vault
- Label: "Disaster Recovery (UK West)"

CONNECTIONS:
- Solid blue arrows for primary traffic flow
- Dashed lines for VNet peering
- Private Link connections shown as secure tunnels
- Redis Cache connected to APIM with bidirectional arrow labeled "Semantic Cache"

ANNOTATIONS:
- "MCSB v2 Compliant" badge in top-right corner
- "50 PTU Total (30/10/10)" label near OpenAI
- "Redis LRU Cache" label near Redis icon
```

---

## Diagram 2: Network Flow Diagram

**Filename**: `uklifelabs_network_flow_corporate.png`

**Prompt**:
```
Create a detailed network flow diagram for the AI Fortress architecture in Microsoft Azure style:

STYLE:
- Clean, light, corporate aesthetic
- White background
- Azure blue (#0078D4) for primary flows
- Green (#107C10) for allowed traffic
- Subnet boxes with light gray borders

LAYOUT (Left to Right Flow):

LEFT - EXTERNAL USER:
- User icon
- Arrow labeled "HTTPS Request"

LAYER 1 - GLOBAL EDGE:
- Azure Front Door Premium
  - WAF inspection
  - DDoS protection
  - Global caching
- Arrow to Private Link Service

LAYER 2 - HUB (10.100.0.0/16):
- Firewall Subnet (10.100.1.0/26)
  - Azure Firewall Premium
  - IDPS enabled
  - TLS inspection
- Private Endpoint Subnet (10.100.2.0/24)
  - OpenAI Private Endpoint
  - SQL Private Endpoint
  - Storage Private Endpoint
- DNS Resolver Subnet (10.100.3.0/28)
  - Private DNS Resolver

LAYER 3 - SPOKE (10.1.0.0/16):
- App Gateway Subnet (10.1.2.0/24)
  - Application Gateway (AGIC)
- AKS Subnet (10.1.1.0/24)
  - AKS Nodes (private IPs)
  - Pod network
- AI Backend Subnet (10.1.3.0/24)
  - APIM Internal
  - Redis Cache (10.1.4.0/28) - NEW SUBNET
- Show Redis Cache with label "Semantic Cache (LRU)"

LAYER 4 - AI SERVICES:
- Azure OpenAI (Private)
  - 3 deployment boxes:
    - "gpt4-prod-deployment (30 PTU)"
    - "gpt4-test-deployment (10 PTU)"
    - "gpt4-dev-deployment (10 PTU)"

TRAFFIC FLOWS:
1. User → Front Door (public HTTPS)
2. Front Door → Private Link Service (Microsoft backbone)
3. PLS → App Gateway (private)
4. App Gateway → AKS Pods (private)
5. AKS → APIM (private)
6. APIM ↔ Redis Cache (cache lookup/store) - HIGHLIGHT THIS
7. APIM → OpenAI Private Endpoint (private)
8. Response flows back in reverse

ANNOTATIONS:
- "All traffic private after Front Door" callout
- "Redis cache hit <50ms" label
- "Private Link DNS resolution via Hub" note
- Fix spelling: "Centralized" (not "Cenbalised"), "Critical" (not "Clltical"), "Spokes" (not "spakes")
```

---

## Diagram 3: Security Flow Diagram

**Filename**: `uklifelabs_security_flow_corporate.png`

**Prompt**:
```
Create a security defense-in-depth diagram for the AI Fortress in Microsoft Azure style:

STYLE:
- Clean, professional corporate style
- Light background
- Security layers shown as concentric shields
- Azure blue for secure components
- Red for threat indicators (blocked)

LAYOUT (Concentric Defense Layers):

OUTER LAYER - PERIMETER:
- Azure Front Door Premium
  - WAF rules (OWASP Top 10)
  - DDoS protection
  - Bot detection
- Show blocked threats in red (SQL injection, XSS)

LAYER 2 - NETWORK SECURITY:
- Azure Firewall Premium
  - IDPS (Intrusion Detection/Prevention)
  - TLS inspection
  - Threat intelligence
- NSG rules on all subnets
- Show allowed traffic in green, denied in red

LAYER 3 - IDENTITY & ACCESS:
- Hybrid Identity flow:
  - On-Prem AD → Entra Connect → Entra ID
- Managed Identities for all services
- Conditional Access policies
- RBAC enforcement
- Show "No API Keys" badge

LAYER 4 - DATA PROTECTION:
- Azure Key Vault (center)
  - TLS certificates
  - Secrets management
  - Key rotation
- Encryption at rest (all storage)
- Encryption in transit (TLS 1.2+)

LAYER 5 - AI GOVERNANCE:
- APIM Policies:
  - PII masking
  - Token throttling
  - Request validation
- Redis Cache (show as optimization, not security)
- PTU isolation (30/10/10)

LAYER 6 - COMPLIANCE:
- Azure Policy enforcement
- MCSB v2 initiative (420+ controls)
- Continuous compliance monitoring
- Audit logging to Log Analytics

CENTER - PROTECTED ASSET:
- Azure OpenAI (Private)
- "Zero Public Access" badge

ANNOTATIONS:
- "Defense in Depth" title
- "MCSB v2 Compliant" badge
- "Zero Trust Architecture" label
```

---

## Diagram 4: Service Journey - User Request Flow

**Filename**: `uklifelabs_service_journey_corporate.png`

**Prompt**:
```
Create a step-by-step service journey diagram showing a user request flow through the AI Fortress:

STYLE:
- Clean, modern, corporate style
- Horizontal flow (left to right)
- Numbered steps (1-10)
- Azure blue for active steps
- Light gray for components

JOURNEY STEPS (Left to Right):

STEP 1 - USER REQUEST:
- User icon
- "Submit AI Query"
- Timestamp: T+0ms

STEP 2 - GLOBAL EDGE:
- Azure Front Door
- "WAF Inspection"
- Timestamp: T+5ms

STEP 3 - FIREWALL INSPECTION:
- Azure Firewall Premium
- "IDPS Scan"
- Timestamp: T+10ms

STEP 4 - GATEWAY:
- Application Gateway
- "TLS Termination"
- Timestamp: T+15ms

STEP 5 - APPLICATION:
- AKS Pod
- "Business Logic"
- Timestamp: T+20ms

STEP 6 - API GATEWAY:
- APIM Internal
- "Policy Enforcement"
- Timestamp: T+25ms

STEP 7 - CACHE LOOKUP (NEW):
- Redis Cache
- Decision diamond: "Cache Hit?"
  - YES → Return cached response (T+30ms) - FAST PATH
  - NO → Continue to Step 8 - SLOW PATH

STEP 8 - AI INFERENCE (if cache miss):
- Azure OpenAI
- "GPT-4 Processing"
- Route to deployment based on X-Environment header:
  - Prod → 30 PTU
  - Test → 10 PTU
  - Dev → 10 PTU
- Timestamp: T+2000ms

STEP 9 - CACHE STORE:
- Redis Cache
- "Store Response (1hr TTL)"
- Timestamp: T+2005ms

STEP 10 - RESPONSE:
- User icon
- "Receive AI Response"
- Timestamp: T+2010ms (first request) or T+30ms (cached)

ANNOTATIONS:
- "Cache hit: 98% faster" callout
- "PTU ensures no throttling" note
- "All traffic private" badge
```

---

## Diagram 5: DR Failover Journey

**Filename**: `uklifelabs_dr_failover_journey_v5_corporate.png`

**Prompt**:
```
Create a disaster recovery failover journey diagram for the AI Fortress:

STYLE:
- Clean, corporate style
- Two-region layout (UK South → UK West)
- Red for failure, green for recovery
- Timeline flow (top to bottom)

LAYOUT:

TOP - NORMAL OPERATIONS (UK South):
- Azure Front Door (global)
- Primary region components:
  - AKS cluster (active)
  - APIM (active)
  - Redis Cache (active)
  - OpenAI (active)
  - SQL Database (primary)
  - Storage (GRS)
- All components in green (healthy)

MIDDLE - DISASTER EVENT:
- Large red "X" over UK South region
- "Regional Outage Detected" alert
- Timestamp: T+0

FAILOVER SEQUENCE (numbered steps):

STEP 1 (T+30s):
- Azure Front Door detects health probe failure
- "Automatic Traffic Rerouting" label

STEP 2 (T+1m):
- Traffic redirected to UK West
- "DNS Update Propagation" label

STEP 3 (T+2m):
- Standby AKS cluster activated
- ACR geo-replicated images pulled locally
- "Container Registry Geo-Replication" callout

STEP 4 (T+5m):
- SQL Database failover (if using failover groups)
- Storage accessible via GRS
- "Data Layer Recovery" label

STEP 5 (T+10m):
- APIM redeployed (or standby activated)
- Redis Cache rebuilt (cache is ephemeral, acceptable loss)
- "Service Layer Recovery" label

STEP 6 (T+15m):
- OpenAI requests routed to UK West deployment
- "AI Layer Recovery" label

BOTTOM - RECOVERY COMPLETE (UK West):
- All components in green (healthy)
- "RTO: 15 minutes" badge
- "RPO: Near-zero (GRS)" badge

ANNOTATIONS:
- "Automated Failover" title
- "ACR Geo-Replication ensures local image availability" note
- "Redis cache rebuilt from cold start (acceptable)" note
```

---

## Diagram 6: APIM Caching Architecture

**Filename**: `uklifelabs_apim_redis_caching_architecture.png`

**Prompt**:
```
Create a detailed APIM + Redis caching architecture diagram:

STYLE:
- Technical, detailed style
- White background
- Azure blue for components
- Green for cache hits, orange for cache misses

LAYOUT (Top to Bottom):

TOP - REQUEST INGRESS:
- AKS Pod
- HTTP Request with headers:
  - X-Environment: prod|test|dev
  - Prompt: "What is Azure?"

LAYER 1 - APIM INBOUND POLICY:
- Policy box showing:
  ```xml
  <cache-lookup caching-type="external">
    <vary-by-query-parameter>prompt</vary-by-query-parameter>
  </cache-lookup>
  ```
- Decision diamond: "Cache Hit?"

CACHE HIT PATH (LEFT - GREEN):
- Arrow to Redis Cache
- "Retrieve from Redis"
- Response time: <50ms
- Skip OpenAI entirely
- Return cached response

CACHE MISS PATH (RIGHT - ORANGE):
- Arrow to Backend Service Selection
- Environment-based routing:
  - X-Environment=prod → gpt4-prod-deployment (30 PTU)
  - X-Environment=test → gpt4-test-deployment (10 PTU)
  - X-Environment=dev → gpt4-dev-deployment (10 PTU)

LAYER 2 - OPENAI PROCESSING:
- Azure OpenAI
- GPT-4 inference
- Response time: 2000ms

LAYER 3 - APIM OUTBOUND POLICY:
- Policy box showing:
  ```xml
  <cache-store duration="3600" caching-type="external" />
  ```
- Store response in Redis

LAYER 4 - REDIS CACHE:
- Azure Redis Cache Premium
- Key structure: hash(prompt + params)
- TTL: 3600 seconds (1 hour)
- Eviction policy: allkeys-lru

BOTTOM - RESPONSE:
- Return to AKS Pod
- Response time: 50ms (hit) or 2000ms (miss)

ANNOTATIONS:
- "Cache hit rate: 70-80% typical" note
- "Saves PTU capacity and reduces latency" callout
- "LRU eviction ensures fresh responses" note
```

---

## Usage Instructions

1. **Image Generation**: Use each prompt with an AI image generation tool (DALL-E, Midjourney, or similar)
2. **Manual Creation**: Use tools like draw.io, Visio, or Lucidchart with the prompts as specifications
3. **File Naming**: Save generated images with the exact filenames specified
4. **Deployment**: Copy images to `c:\MyResumePortfolio\assets\img\`
5. **Verification**: Ensure all spelling errors are corrected (Centralized, Critical, Spokes, OpenAI, etc.)

---

## Checklist

- [ ] Diagram 1: Complete Solution Overview
- [ ] Diagram 2: Network Flow (with Redis subnet)
- [ ] Diagram 3: Security Flow (with MCSB v2)
- [ ] Diagram 4: Service Journey (with cache hit/miss paths)
- [ ] Diagram 5: DR Failover Journey
- [ ] Diagram 6: APIM + Redis Caching Architecture (NEW)
- [ ] All spelling errors corrected
- [ ] All diagrams use consistent Microsoft corporate style
- [ ] Redis Cache prominently featured where applicable
- [ ] PTU split (30/10/10) clearly shown

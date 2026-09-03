---
title: "Pick the Wrong Compute, Pay Forever: A Practical Azure AI Hosting Decision Tree"
date: 2026-01-10
tags: ["Azure", "Azure AI", "Azure OpenAI", "Azure Container Apps", "AKS", "APIM", "Landing Zones", "Security", "Architecture"]
---

Mr. Technical Consultant opened the Agent Dashboard for ZionPay.

Yesterday, the demo was clean.

Today, one graph was not.

**Token spend was rising, fast.**

Mr. Project Manager pinged.
“Plan by Friday. What are we hosting on. AKS or something simpler. One answer.”

Mr. Cloud Engineer replied.
“Pick the platform. I build today.”

Mr. Cloud Architect added.
“Landing zone first. Private endpoints, DNS, egress, no shortcuts.”

Then Mr. Customer asked the only question that matters.
“If this goes viral, do we stay in control, or do we burn money and trust?”

Mr. Technical Consultant knew the trap.
Teams pick compute by habit.
AI punishes that.

So he wrote one line on the whiteboard.

**Compute is not where you run containers. Compute is how you control cost, scale, and blast radius.**

---

## The cast
- **Mr. Technical Consultant**: removes ambiguity, locks decisions, prevents surprises.
- **Mr. Project Manager**: wants dates, ownership, and a deck that survives Q&A.
- **Mr. Cloud Architect**: enforces landing zone guardrails and security posture.
- **Mr. Cloud Engineer**: ships the build and hates rework.
- **Mr. Customer**: wants control, auditability, and predictable outcomes.

---

## The constraints template (copy/paste)
If you skip this, you will replatform twice.

**Security and network**
- Entry: public internet, private-only, or both
- Private endpoints required for model and data: yes/no
- Hybrid connectivity: ER/VPN yes/no
- Egress: open, restricted, or forced tunneling

**Scale**
- Peak RPS and concurrency
- Traffic pattern: steady / bursty / unpredictable
- Cold-start tolerance: <1s, 1–5s, >5s

**Compute**
- GPU needed: now / later / never
- Runtime type: real-time API / async worker / batch

**Ops**
- Do we have an AKS platform team and on-call: yes/no

**Cost control**
- Token quota enforcement at gateway: yes/no
- Chargeback/showback required: yes/no

---

## The decision tree (one-screen version)

```text
START
  |
  |-- Do you need Kubernetes-only features?
  |      (service mesh, complex scheduling, multi-tenant cluster governance,
  |       large dedicated GPU pools, strict node-level control)
  |         |-- YES --> AKS
  |         |-- NO  --> continue
  |
  |-- Is traffic bursty or unpredictable?
  |         |-- YES --> Azure Container Apps (ACA)
  |         |-- NO  --> continue
  |
  |-- Is it a simple "run and exit" CPU job?
  |         |-- YES --> ACI (CPU only)
  |         |-- NO  --> ACA by default
```

### Thresholds that stop debates
- If you need **sub-second latency** and **high sustained throughput** and you have a platform team, AKS is justified.
- If you have **bursts, idle periods, or uncertain demand**, ACA is usually the right default.
- If it is **batch + CPU** and you can “run and exit”, ACI is fine.
- If it is **GPU**, do not use ACI. Do ACA serverless GPU or AKS GPU pools.

---

## The non-negotiable rulebook (the part that saves you)
Mr. Customer did not care about AKS vs ACA.
He cared about **control**.

So Mr. Technical Consultant drew this.

```text
Clients/Apps
   |
   v
APIM (One Rulebook)
   - Entra ID auth (JWT validation)
   - Token quota + rate limits
   - Tool allowlist (only approved downstream APIs)
   - Audit logs + correlation IDs
   |
   v
Compute (ACA/AKS) -> Model + Data (prefer Private Endpoints)
```

If your apps call model endpoints directly, you do not have an AI platform.
You have an uncontrolled spend pipe.

---

## Before scenarios: one APIM trap to avoid
People say “APIM internal” without saying what tier and what networking model.

Add this paragraph to prevent wrong builds:

- If you need a **private-only gateway** for consumers, you need the **APIM internal VNet mode pattern** (classic injected networking).
- If you use **v2 tiers with outbound VNet integration**, treat it as “private to backend”, not “private to consumers”.
- Do not assume Private Endpoint magically makes APIM “internal”. Read the APIM networking limitations first.

This single clarification prevents weeks of rework.

---

# Five scenarios. Five reference architectures.
Each scenario uses the same template so readers can act.

## Scenario 1: Internal-only agents (regulated enterprise)
**When**
Employee copilots, internal knowledge agents, regulated data.

**Non-negotiable constraints**
- Private-only entry
- Private endpoints for model and data
- Egress controlled

**Bill of materials**
- APIM internal pattern (private gateway)
- ACA in VNet-integrated environment
- Azure OpenAI with Private Endpoint + Private DNS
- Key Vault for secrets
- Central logging (App Insights + SIEM)

**Critical policies**
- `validate-jwt` or `validate-azure-ad-token`
- Token quota policy at APIM
- Tool allowlisting at APIM

**What breaks first (plan for it)**
- DNS mistakes on Private Endpoints
- Outbound egress not matching dependency needs
- “Temporary allow” rules that become permanent

**90-minute lab outcome**
A private agent API in ACA, fronted by APIM, calling a model endpoint through Private Link.

---

## Scenario 2: Internet-facing customer AI (public entry, private model/data)
**When**
Customer chat, partner agent APIs, public portals.

**Non-negotiable constraints**
- WAF at the edge
- Hard throttling
- Model + data kept private

**Bill of materials**
- WAF (App Gateway WAF or your edge standard)
- APIM as the only public API surface
- ACA for runtime
- Private endpoints to model and data

**Critical policies**
- Token quota policy is mandatory
- Bot/abuse throttling at gateway
- Request size limits and payload validation

**What breaks first**
- Public endpoints accidentally left enabled on model/data
- Missing per-client quotas, one tenant eats the whole budget
- No audit trail when something goes wrong

**90-minute lab outcome**
Public endpoint protected by WAF and APIM, backend is private.

---

## Scenario 3: Hybrid agents (Azure runtime + on-prem tools)
**When**
Agent must call on-prem systems (CMDB, ITSM, legacy APIs).

**Non-negotiable constraints**
- ER/VPN required
- One policy surface for both cloud and on-prem calls

**Bill of materials**
- APIM in a controlled network path to on-prem
- ACA runtime in same network boundary
- Tool APIs behind allowlisted routes
- Central observability

**What breaks first**
- Asymmetric routing between cloud and on-prem
- Firewall ownership confusion during cutover
- Latency to on-prem tools causing agent timeouts

**90-minute lab outcome**
An agent that calls one on-prem API and one Azure API, both governed by the same APIM rulebook.

---

## Scenario 4: GPU skills without becoming an AKS platform team
**When**
Vision, heavy embeddings, GPU bursts, custom inference.

**Non-negotiable constraints**
- GPU needed for specific skills
- You want scale-to-zero economics

**Bill of materials**
- APIM front door with quotas
- ACA serverless GPU workers for GPU skills
- Premium container registry and small images to reduce cold start
- Private endpoints where required

**What breaks first**
- Image size and cold start
- GPU quotas in region
- Long-running requests without timeouts and retries

**90-minute lab outcome**
A GPU “skill endpoint” behind APIM, autoscaling based on demand.

---

## Scenario 5: Batch pipelines and offline jobs
**When**
Backfills, re-embedding runs, nightly summarization.

**Non-negotiable constraints**
- Non-interactive
- Cost optimized
- Run and exit

**Bill of materials**
- ACI for CPU batch tasks, or ACA jobs/worker pattern for event-driven runs
- Storage for artifacts
- Central logging

**What breaks first**
- Lack of idempotency (reruns duplicate data)
- No run metadata (can’t prove what happened)
- Hidden dependency on interactive services

**90-minute lab outcome**
A job that runs on a schedule, logs output, and exits cleanly.

---

## The moment it clicked
Mr. Project Manager asked, “What do we tell the client?”

Mr. Technical Consultant wrote the final decision:

- Default runtime: **Azure Container Apps**
- Default enforcement: **APIM rulebook (identity + quotas + audit)**
- AKS only when a real Kubernetes-only need exists
- ACI only for simple CPU run-and-exit jobs

Mr. Cloud Architect nodded. “Now I can lock guardrails.”
Mr. Cloud Engineer nodded. “Now I can build without rework.”
Mr. Customer nodded. “Now I can trust the rollout.”

---

# Practical checklist
1) Put APIM in front of every model call and tool API.
2) Use Entra ID at the gateway. Do not distribute model keys.
3) Enforce token quotas and rate limits per client.
4) Emit token metrics and correlate requests end-to-end.
5) Use ACA unless you have a proven AKS platform requirement.
6) Keep model and data private where required. Get Private DNS right.
7) Treat DNS, egress, and quotas as production features, not “later”.

---

# Resource vault (curated, high signal)

## Start here (3 links)
```text
ACA scaling (KEDA-backed scale rules)
https://learn.microsoft.com/en-us/azure/container-apps/scale-app

APIM JWT validation policy (identity at the gateway)
https://learn.microsoft.com/en-us/azure/api-management/validate-jwt-policy

Limit Azure OpenAI token usage in APIM
https://learn.microsoft.com/en-us/azure/api-management/azure-openai-token-limit-policy
```

## Build labs (6 links)
```text
AI-Gateway sample (APIM policy patterns for AI)
https://github.com/Azure-Samples/AI-Gateway

GenAI gateway with APIM
https://github.com/Azure-Samples/genai-gateway-apim

APIM + Azure OpenAI reference implementation
https://github.com/microsoft/AzureOpenAI-with-APIM

Enterprise logging for OpenAI usage
https://github.com/Azure-Samples/openai-python-enterprise-logging

RAG reference app (Azure AI Search + Azure OpenAI)
https://github.com/Azure-Samples/azure-search-openai-demo

Smart load balancing policy pattern (archived, still useful to learn)
https://github.com/Azure/apim-aoai-smart-loadbalancing
```

## Watch (4 videos)
```text
Run open models on Serverless GPUs (NVIDIA NIM on ACA)
https://www.youtube.com/watch?v=GvZJHHCk244

Microsoft & NVIDIA: Accelerating AI with NVIDIA NIM on Azure
https://www.youtube.com/watch?v=m3lip7wCyzQ

Azure AI Search with a custom GPT-4 Vision skill
https://www.youtube.com/watch?v=VPxdqlcblYU

Secure and scale your AI APIs with Azure API Management
https://www.youtube.com/watch?v=HuPNgrjMcuI
```

---

## One-line takeaway
If you pick compute without constraints and ship agents without a gateway rulebook, you do not have an AI platform.

You have a cost leak.

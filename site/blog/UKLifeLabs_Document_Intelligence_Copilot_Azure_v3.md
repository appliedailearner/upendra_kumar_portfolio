---
title: "UKLifeLabs Document Intelligence Copilot on Azure"
date: 2026-01-17
description: "A deployable Azure AI Landing Zone for regulated document Q&A with citations, audit trail, APIM-first controls, and predictable quota + cost planning."
tags: ["Azure", "Azure AI Foundry", "Azure OpenAI", "APIM", "AKS", "Azure AI Search", "Document Intelligence", "RAG", "Security", "Landing Zone", "Copilot", "Cloudflare", "DevOps", "MCP"]
read_time: "18 min"
---

# UKLifeLabs Document Intelligence Copilot on Azure
## The deployable blueprint that survives audit, load, and cost pressure

```mermaid
flowchart LR
  U[User UI
(Teams / Copilot Studio
Open WebUI
Custom Portal)] -->|HTTPS| APIM[Azure API Management
AI Gateway]
  APIM -->|/chat| ORCH[RAG Orchestrator
(AKS/ACA)]
  APIM -->|/ingest events| ING[Ingestion Workers
(AKS/Functions/ACA)]

  ORCH -->|retrieve| SEARCH[Azure AI Search
(vector + keyword)]
  ORCH -->|generate| AOAI[Azure OpenAI
(deployments in Foundry)]

  ING -->|extract| DI[Document Intelligence]
  ING -->|chunk + embed| EMB[Embeddings]
  EMB --> SEARCH
  DI -->|text + fields| STORAGE[(Storage
ADLS/Blob)]

  ORCH --> AUDIT[(Audit Store
append-only)]
  APIM --> AUDIT
  STORAGE --> SEARCH

  subgraph Network boundary (private)
    APIM
    ORCH
    ING
    SEARCH
    AOAI
    DI
    STORAGE
    AUDIT
  end
```

---

## TL;DR (30 seconds)
UKLifeLabs needs employees to upload large document packs and ask questions.

But answers must be:
- provable (citations)
- traceable (audit trail)
- access-controlled (no leakage)
- cost-controlled (no runaway spend)

This blog gives you a buildable reference architecture:

**UI → APIM (AI Gateway) → RAG Orchestrator → AI Search → Azure OpenAI + Document Intelligence → Citations + Audit**

## Design principles (the Microsoft review-board version)
1) **APIM-first boundary**: no direct calls from UI to Search, models, or ingestion.
2) **Two-lane architecture**: chat stays fast, ingestion stays heavy and async.
3) **Evidence-or-refusal**: answers must include citations (or the system refuses).
4) **Least privilege by default**: retrieval filters enforce the user's access.
5) **Cost is a control plane concern**: token budgets and rate limits are enforced at APIM.
6) **Operationally boring**: everything is observable, alertable, and repeatable as code.

## Threat model (what can go wrong)
- **Data leakage**: a user queries content they should not see. Fix: security trimming + group-based filters at retrieval.
- **Prompt injection**: docs contain malicious instructions. Fix: strip instructions, isolate retrieved text, enforce tool allowlist.
- **Runaway spend**: unconstrained token usage. Fix: quotas, budgets, max payload size, and per-product throttling.
- **Availability**: ingestion swamps runtime. Fix: separate compute pools and backpressure.
- **Audit failure**: no trace of why an answer was produced. Fix: store prompt hash, chunk IDs, model deployment ID, and correlation IDs.


---

## What’s in scope
✅ In scope
- Upload PDFs and office docs
- Extract fields + full text
- Chunk + index for RAG
- Chat with citations and evidence
- Full audit trail per question
- Internal-only deployment, with optional external access lane

❌ Out of scope (Wave 1)
- Training/fine-tuning for “learning the whole org”
- Complex multi-agent workflows
- Replacing the enterprise DMS
- Full DLP/IRM integration (can be Phase 2)

---

## The Airport + Research Library analogy (easy to remember)
This platform is a secure airport with a library inside.

- UI is the check-in counter
- APIM is immigration + security + the power meter
- AI Search is the library catalog
- Azure OpenAI is the expert panel
- Document Intelligence is the baggage scanner
- Storage is the vault

Rule:
**Nobody reaches the experts without passing security.**

---

## Sizing (what we build for)
| Metric | Value |
|---|---:|
| Employees | 6,500 |
| Target users (Year 1) | 700 |
| Peak concurrent | 60 |
| Peak traffic | 140 req/min (120 internal + 20 external) |
| Backlog docs | 1.8M (~12TB) |
| New docs/day | 8,000 |
| Freshness target | 15 minutes |

What this means:
- ingestion must be async
- chat must stay responsive
- external traffic must not impact internal users

---

# The architecture (practical reference stack)

## 1) UI layer (pick ONE)
UI is replaceable. The boundary is not.

**Option A: Open WebUI**  
Fastest “don’t build UI from scratch” route.  
Treat it like a product. Patch it. Harden it.

**Option B: Microsoft-native UI**  
Best for enterprise adoption:
- Copilot Studio (low-code rollout)
- Teams-based copilot experience

**Option C: Custom portal**  
Best long-term control:
- upload workflow
- citations panel
- audit viewer
- role-based experiences

---

## 2) APIM is the AI Gateway (non-negotiable)

### Network and key management baseline (do this before feature work)
For regulated workloads, treat connectivity as part of the product:
- **Private access**: keep AI Search, Storage, and orchestration on private networks. Use private endpoints where available.
- **Certificates and secrets**: store in **Key Vault**. Do not keep PFX files in repos or build agents.
- **Outbound control**: restrict egress from the runtime so it cannot call arbitrary internet endpoints.
- **DNS hygiene**: document private DNS zones and forwarding. Broken DNS is the #1 private endpoint failure mode.

APIM is the platform control plane.

It enforces:
- JWT validation (identity gate)
- rate limits (traffic control)
- token budgets (cost control)
- request guardrails (safety control)
- audit logs (traceability)

---

## JWT validation (simple and sticky)
JWT is a tamper-proof boarding pass.

APIM checks:
1) Is it real? (issuer + signature)
2) Is it expired?
3) Is it meant for this API? (audience)
4) Is the user allowed? (claims/groups)

Fail any check:
Access is denied.

---

## 3) Runtime layer (AKS vs ACA)
**Recommendation: use AKS for production.**

Use ACA only for pilot if you need speed.

AKS fits regulated enterprise patterns:
- tighter network segmentation
- better control for multi-service workloads
- predictable performance under sustained load

Simple rule:
- regulated platform → AKS
- fast demo → ACA

---

## 4) Data + RAG layer
This is where “truth” lives.

- ADLS Gen2 / Blob
  - raw documents
  - extracted JSON
  - audit artifacts

- Document Intelligence
  - extracts text and fields for PDFs and scans

- Azure AI Search (Standard S1+)
  - chunk index + metadata + vector search
  - scale using partitions/replicas as demand grows

For ingestion, integrated vectorization reduces custom glue code.

---

## 5) Model layer (Azure AI Foundry / Azure OpenAI)
Recommended model set:
- GPT-4o for chat + summarization
- Reasoning model only for “high-stakes checks”
- text-embedding-3-large for embeddings

Use managed identity wherever possible.
Avoid secrets.

---

# The two flows you must separate (this prevents production pain)

## Flow A: Chat (user-facing, low latency)
1) UI → APIM `/v1/private/chat`
2) APIM validates JWT + limits
3) Orchestrator queries AI Search with access filters
4) Orchestrator calls Azure OpenAI with retrieved chunks
5) Response returns with citations
6) Audit log saved

## Flow B: Ingestion (async, heavy workload)
1) Document lands in storage `landing/`
2) Event triggers ingestion worker
3) Document Intelligence extracts text + fields
4) Chunking + embeddings
5) Index into AI Search
6) Store extracted JSON and trace into `audit/`

This separation is what keeps chat stable.

---

# “Citations required” rule (the regulated mode)
This is the line that matters.

If citations are missing:
- the model response is incomplete
- the system must refuse to finalize

Rule:
**No citations, no final answer.**

This alone makes your copilot audit-friendly.

---

# Security trimming (do not skip this)

## Audit trail: minimum fields (what auditors will ask for)
Store one record per user question and one per ingestion job.

**Chat audit record (minimum):**
- `correlationId`, `timestamp`, `environment`
- `userId` (or pseudonymous ID), `tenantId`, `clientAppId`
- `groupIdsSnapshot` (or role names) used for retrieval filtering
- `request`: prompt hash, input size, route (`/private/chat` vs `/public/chat`)
- `retrieval`: index name, query params, topK, **chunkIds + docIds returned**
- `generation`: model deployment ID, temperature, max tokens
- `usage`: prompt tokens, completion tokens, total tokens
- `latencyMs`: end-to-end, plus Search and model call latency
- `result`: citations present (true/false), refusal reason if refused

This is how you prove: who asked, what they were allowed to see, what evidence was used, and which model produced the output.

RAG must enforce permissions at retrieval time.

Every chunk should carry:
- department
- classification
- owner
- allowedGroups
- retentionTag
- sourceSystem

Every query should filter by:
- user Entra groups
- allowed classification
- department scope

If you skip this, you will leak data across teams.

---


# Quota planning (TPM/RPM) so you do not get throttled
You do not plan quota by gut feel. You plan it by **(requests per minute) x (tokens per request)** plus headroom.

## Step 1: pick realistic token ranges
Token usage depends on doc length, chunk count, and answer size. Use scenarios:
- Small Q&A: **1,200-2,000** tokens
- Typical RAG Q&A: **2,000-4,000** tokens
- Heavy Q&A (long context, long answer): **4,000-8,000** tokens

## Step 2: compute TPM
Given your sizing targets:
- Peak requests/min: **140**
- Plan tokens/request: **3,000** (typical)

Estimated TPM = 140 x 3,000 = **420,000 TPM**
Add 25-35% headroom for spikes, retries, and safety: **~550,000 TPM**

## Suggested starting quota ask (Wave 1)
- Interactive chat deployments: **550k TPM**
- Embeddings deployments: **300k TPM**
- Batch summarization (optional): **250k TPM**

Total starting ask: **~1.1M TPM** split across deployments so one workload cannot starve the other.

Operational rule: if you see frequent 429s, either (a) raise quota, (b) lower max tokens, or (c) add throttling per product.
---

# PTU vs TPM/RPM vs Fine-tuning quota (clean explanation)

## Deployment quota (TPM/RPM/PTU)
This controls runtime traffic.

- RPM = how many cars enter per minute
- TPM = how much fuel burns per minute
- PTU = reserved private lanes (predictable, paid)

Use PTU when:
- stable latency is required
- usage is steady and business-critical

## Fine-tuning quota
This controls training jobs, not runtime traffic.

Analogy:
- deployment quota = how many flights today
- fine-tuning quota = how many pilot training sessions this month

For document Q&A:
RAG quality beats fine-tuning in Wave 1.

---

# APIM policy baseline (minimum viable production pack)
These are the “airport controls”.

1) JWT validation (identity gate)
2) Rate limit per product/client (traffic control)
3) Token budgets (TPM caps)
4) Prompt caps (max input size)
5) Response caps (max output size)
6) Audit logs (user, tokens, latency, model deployment)

---


# Practical implementation accelerators (ship faster)

## A) APIM Landing Zone Accelerator (IaC)
If you need repeatable Dev/Test/Prod APIM, use an ALZ-aligned IaC accelerator.

What it gives you:
- Bicep modules for APIM + identity + monitoring (and room to extend networking)
- a centralized settings file per environment
- an Azure Developer CLI workflow (azd) to provision consistently

How to apply it to this copilot:
- Deploy APIM first as the hard boundary.
- Create Products (internal vs external) as code.
- Put policies into policy fragments and version them.
- Promote Dev -> Test -> Prod via pipeline, not portal clicks.

## B) APIM as an MCP Gateway (Phase 2 pattern)
If you plan agentic tooling later, APIM can sit in front of MCP servers.

Why it matters:
- You govern tool access like APIs (identity, quotas, audit).
- You can support On-Behalf-Of (OBO) so the agent uses the user identity.

Minimal target state:
- MCP server hosted on Azure Functions (or a container).
- APIM in front as the MCP gateway.
- Identity validation at APIM.
- OBO flow for sensitive downstream calls (example: Microsoft Graph).

## C) Custom domain with Cloudflare (branded endpoint)
If your domain already sits on Cloudflare, this is a clean path.

Steps:
1) Create a Cloudflare Origin SSL certificate for your API hostname.
2) Convert it to a PFX (or store it in Key Vault for production).
3) Attach the hostname in APIM Custom Domains.
4) Create a CNAME in Cloudflare pointing to the APIM gateway hostname.
5) Keep the Cloudflare proxy disabled for that CNAME.

Production note:
- Treat the private key as a secret and store it in Key Vault.

## D) DevOps baseline for APIM (regulated environments)
Treat APIM like code.

Practical repo layout:
- `/infra/`  APIM + dependencies (Bicep/Terraform)
- `/apim/`   APIs, products, named values, policy fragments
- `/pipelines/`  validate, deploy, smoke test

Rules that prevent drift:
- No portal edits in Prod.
- Dev/Test/Prod deployments are promoted from the same repo.
- Changes require PR review + approvals.

---

# Content Safety (internal vs external)
Internal users:
- default filters + full logging
- block jailbreak attempts

External users:
- stricter filtering
- tighter output limits
- stronger throttling

Hard rule stays:
No citations, no final answer.

---

# Do we need external WAF + App Gateway?
Decision rule:
- internal-only users → skip external WAF
- external access required → add WAF lane

Only add external exposure when business proves the need.

---

# One APIM or two?
Start with one APIM.

Split by Products:
- Product A: internal employees
- Product B: external users

Different limits per product:
- internal higher
- external lower

Go to two APIM instances only if external noise threatens internal availability.

---

# Cost reality (what will dominate spend)
Be honest here.

Top cost drivers:
1) model tokens (chat + embeddings)
2) Search scaling (partitions + replicas)
3) external WAF/App Gateway fixed cost (if enabled)
4) ingestion compute for backlog

Token budgets in APIM are the cheapest way to prevent runaway spend.

---

# What fails in production (learn from others)
1) stale index = wrong answers
2) ingestion steals capacity from chat
3) missing quotas = throttling
4) no token budgets = surprise bill
5) no security trimming = data leak
6) citations missing = audit failure

---


# Operations (what makes this production-grade)
Treat this like a platform, not a demo.

## SLOs (set targets early)
- Chat p95 latency (internal): target and track
- Ingestion freshness: **15 minutes** end-to-end for newly landed docs
- Answer quality: citation coverage rate, refusal rate, user feedback score
- Availability: APIM + runtime uptime

## Dashboards you should have on day 1
- Requests/min by product (internal vs external)
- Token usage and cost proxy by product
- 429 rate (throttling) and 5xx rate
- Search latency, model latency, and end-to-end latency
- Ingestion backlog depth and processing rate

## Runbooks that save you during incidents
- "Users cannot access docs" (group filters / index metadata)
- "Citations missing" (index freshness / retrieval failure)
- "Throttling" (quota, max tokens, APIM limits)
- "Bad answers" (chunking rules, topK, prompt template)


# Deployment plan (Wave 1 in 14–30 days)

## Week 1: Boundary + skeleton
- APIM deployed
- routes created
- JWT validation stubbed
- baseline networking ready

## Week 2: RAG core
- AI Search Standard tier deployed
- indexing pipeline created
- citations enforced

## Week 3: Ingestion + extraction
- Document Intelligence extraction pipeline
- chunking + embeddings
- freshness target validated (15 minutes)

## Week 4: Hardening + go-live
- strict throttles
- token budgets
- audit validation
- operational dashboard

---

# Go-live checklist (copy-paste)
- [ ] UI calls APIM only
- [ ] JWT validation enabled for private and public routes
- [ ] APIM Products split (internal vs external)
- [ ] Rate limits + token budgets enabled
- [ ] Prompt + response caps enforced
- [ ] Citations required rule enabled
- [ ] Two lanes built (chat vs ingestion)
- [ ] Search schema includes permissions
- [ ] Retrieval enforces access filters
- [ ] Audit logs include chunk IDs + model deployment ID
- [ ] Freshness dashboard is live

---

# Starter kit you should attach to this blog
Make this blog “usable tomorrow”.

- 01-Architecture/
  - flow diagram
  - AKS vs ACA decision tree
  - endpoint naming map
- 02-APIM-Policy-Pack/
  - JWT policy
  - throttles
  - token budget configs
- 03-RAG/
  - index schema template
  - chunking rules
  - citation response format
- 04-Ingestion/
  - backlog vs realtime strategy
  - extraction schema
- 05-Runbook/
  - validation tests
  - operational metrics
  - troubleshooting guide

- 06-APIM-Accelerators/
  - IaC baseline (Bicep/azd or Terraform)
  - policy-as-code structure
  - environment promotion checklist
- 07-MCP-Gateway/
  - MCP gateway pattern with APIM
  - OBO flow checklist
  - tool allowlist template
- 08-Domains-Certs-DNS/
  - custom domain runbook (Cloudflare example)
  - certificate handling checklist

---


## References and field-tested examples

**Community resources (useful patterns, not official Microsoft guidance):**
- APIM Landing Zone Accelerator (Bicep + azd): https://github.com/Evilazaro/APIM-Accelerator
- MCP + APIM Zero-Trust lab (OBO flow, MCP gateway): https://github.com/thiagomendes/lab-apim-mcp
- Custom domain for APIM using Cloudflare (origin cert + CNAME): https://www.stephenwthomas.com/azure-integration-thoughts/azure-apim-custom-domain-setup-cloudflare/
- APIM DevOps discussion thread (LinkedIn): https://www.linkedin.com/posts/ramathotapalli_azure-apimanagement-devops-activity-7417770342183739392-uYYS

---


## Final takeaway
If you want this to survive a real enterprise review, make four things non-negotiable:
1) **APIM is the boundary** (identity, throttles, budgets, audit).
2) **Two lanes** (chat stays responsive, ingestion stays heavy and async).
3) **Security trimming** (retrieval-time enforcement, no cross-team leakage).
4) **Evidence-or-refusal** (citations are mandatory, always).

Everything else is implementation detail.

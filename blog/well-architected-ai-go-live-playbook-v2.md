---
title: "Well-Architected AI: The \"Go-Live\" Playbook for Production Copilots"
date: 2026-01-19
description: "A production-ready go-live playbook for Azure AI copilots using Azure Well-Architected Framework. Two lanes, one gateway, evidence-or-refusal, audit trails, guardrails, and Day-2 operations."
tags: ["Azure Well-Architected", "Azure AI", "GenAI", "RAG", "APIM", "Security", "Operations", "GenAIOps", "Responsible AI"]
readTime: "14 min"
series: "Document Intelligence Copilot on Azure"
seriesOrder: 3
---

# Well-Architected AI: The "Go-Live" Playbook for Production Copilots

**Series:** Document Intelligence Copilot on Azure (Part 3)  
**Date:** January 19, 2026  
**Cast:** **Upendra** (Lead Architect), **Trinity** (Cloud Engineer), **Morpheus** (Security Architect)

---

## Scene 1: The Question that Matters

**Project Manager:** “We go live next week. Are we production-ready?”

**Trinity:** “The chat works. The ingestion pipeline is moving documents. It looks great in the playground.”

**Morpheus:** “That’s not production, Trinity. That’s just a **working endpoint**. A production system survives an adversary; a demo just survives a presentation.”

**Upendra:** “Morpheus is right. In this new era, 'production' is a high bar. It means being **safe, reliable, cost-controlled, testable, and operable**. Anything else is just compute.”

---

## 1) Why AI Architecture is Different

Traditional software fails in predictable ways. AI applications fail in **surprising ways**:

- **Non-determinism:** the same question might get different answers  
- **Hallucinations:** the model states facts that aren’t in the data  
- **Token runaway:** costs spike quietly as prompts bloat  
- **Prompt injection:** users trick the model into bypassing safety rules  

To counter this, we don’t just code. We **architect guardrails**.

---

## 2) WAF Pillars → Production Guardrails (the reviewer checklist)

Upendra turns “principles” into **controls**. This is what makes the design review easy.

| WAF Pillar | What it means for AI workloads | Wave 1 guardrails to implement |
|---|---|---|
| Reliability | Survive throttling + timeouts + backlogs | Bulkheads (2 lanes), queue-based ingestion, retries/backoff, circuit breaker |
| Security | Prevent data leakage + bypass routes | APIM boundary, private endpoints where required, security trimming, content safety |
| Cost Optimization | Stop silent spend creep | Token budgets at gateway, per-product quotas, caching, PTU strategy |
| Operational Excellence | Run it daily without heroics | Trace IDs, dashboards, runbooks, incident playbooks, versioning |
| Performance Efficiency | Keep p95 stable under load | Retrieval time budget, topK caps, hybrid retrieval, graceful refusal paths |

---

## 3) Reference Architecture: Two Lanes, One Gateway

To prevent downstream chaos, we separate the workload into **two isolated lanes** with one boundary.

- **Ingestion Lane (The Truth Factory)**  
  Documents move from extraction to indexing. We insert a **Queue** for **backpressure**, so upload spikes do not crash Search.

- **Chat Lane (The Intelligence Path)**  
  This is the user path. The UI **never** calls Search or OpenAI directly.

**Why this works:** bulkhead isolation. Ingestion can be on fire and chat still holds p95.

---

## 4) The Five-Layer Model (Stop Building Spaghetti)

Upendra stops the “patchwork architecture” by layering the workload.

| Layer | Responsibility | Azure component |
|---|---|---|
| **1. Client** | UI only, keep it thin | Teams / Web App / Open WebUI |
| **2. Intelligence** | Orchestrator where rules live | Orchestrator API |
| **3. Inferencing** | Model calls + deployment versioning | Azure OpenAI / Foundry |
| **4. Knowledge** | Retrieval + grounding | Azure AI Search + ADLS |
| **5. Tools** | Actions + business APIs | Internal APIs via APIM |

**Rule:** the client is a view. The orchestrator is the brain.

---

## 5) The AI Workload Design Loop (Build → Measure → Adapt)

**Trinity:** “Once deployed, we are done, right?”  
**Upendra:** “In AI, you are never done. You ship, then you correct drift.”

Wave 1 needs this loop:

1) **Build**: prompt, retrieval, policies, limits  
2) **Measure**: citation coverage, refusal rate, p95 latency, token/request  
3) **Adapt**: tuning chunking/retrieval, policy updates, index rebuilds  
4) **Control change**: version prompts, indexes, policies, model deployments

---

## 6) Platform decisions (AKS vs ACA) plus training vs inference compute

### AKS vs ACA (Wave 1)
- **AKS**: best for regulated production patterns (network control, segmentation, multiple internal services)
- **ACA**: good for rapid pilots, fewer ops, but less control for complex enterprise segmentation

### Training vs inference compute (don’t mix these)
- **Inference** should be stable, monitored, and protected behind APIM  
- **Training/fine-tuning** is usually **batch + transient**. Shut it down when idle  
- Use orchestration for complex training workflows (pipelines, data validation, approvals)
- Prefer managed options (Azure ML for lifecycle control). Avoid “always on” serverless for heavy continuous runs

---

## 7) The Three Golden Production Contracts

Upendra insists most copilots fail because they lack clear **contracts**.

### Contract 1: Evidence-or-Refusal
If grounding exists → answer + citations.  
If grounding is missing → **refuse**.

**Enforce it server-side** using a validator. Not just prompt wording.

**Wave 1 validator rules**
- citations must reference real chunk IDs
- citations must map to allowed documents for the user
- refusal if retrieval returns zero trusted chunks

### Contract 2: The Audit Trail
A “200 OK” is not an audit.

Log **what influenced the answer**, queryable by `requestId`:
- user identity
- retrieved chunk IDs and doc IDs
- filters applied (true/false)
- model deployment ID
- index version
- token counts

### Contract 3: Permission-Aware Retrieval
The model is **not** your security boundary. Retrieval is.

**Security trimming must be enforced** using validated identity claims so users only see authorised content.

---

## 8) Grounding data design (quality is a product feature)

**Morpheus:** “Show me the mechanism that prevents cross-team leaks.”  
**Upendra:** “It’s not the model. It’s the metadata and filters.”

### Minimum chunk metadata (Wave 1)
Store these on each chunk:
- `docId`, `chunkId`, `content`, `vector`
- `pageNumber`, `sourcePath`
- `allowedGroups[]` (or ACL tags)
- `classification`, `ingestedAt`, `indexVersion`

### Chunking rules that improve citations
- keep chunks page-aware for citation precision
- prefer semantic boundaries (headings/sections) over raw token splits
- store a snippet preview for audit tools

### Retrieval rules (Wave 1)
- use hybrid retrieval (keyword + vector)
- cap `topK` (3–8) to control latency + hallucination risk
- enforce security trimming server-side
- never accept filter input directly from the user

---

## 9) Data platform decision (keep it simple unless forced)

Don’t build an extra data platform “because AI”.

**Start simple**
- ADLS for raw + extracted JSON + audit artifacts
- AI Search for retrieval + vectors

**Add more only when needed**
- multiple sources and heavy aggregation needs
- source systems cannot handle AI query volume
- governance requires a curated analytical store

**Non-negotiables**
- data lifecycle management
- versioned outputs (index versions)
- auditability + traceability

---

## 10) Operations: monitor signals, not hopes

**Morpheus** won’t sign off until the system has measurable signals.

### Model signals
- refusal rate trend
- p95 latency
- throttle rate (429)

### Cost signals
- token usage per subscription/product
- token cost per route (chat vs ingestion)

### Retrieval signals
- query latency
- index freshness (`now - lastIngestedAt`)
- no-results rate (leads to refusals)

### Ingestion signals
- queue depth
- failures and retries
- processing time per document

---

## 11) Day-2 operating model (owners and responsibilities)

This avoids “who owns it?” fights during incidents.

| Area | Primary owner | What they own |
|---|---|---|
| APIM + identity boundary | Platform team | Auth, rate limits, token budgets, routing, private access |
| Orchestrator API | App team | Prompting, validation, contracts, fallback logic |
| Search + retrieval quality | Data team | Index schema, chunking, filters, freshness, rebuilds |
| Ingestion pipeline | Data team | extraction, chunking, poison queue, retry strategy |
| Security + compliance | Security team | content safety thresholds, audit reviews, policy sign-off |
| Observability + SRE | Ops/SRE | dashboards, alerts, on-call, runbooks |

---

## 12) Testing and Go/No-Go gates

Credibility comes from a **Golden Test Set** of 30–50 questions:
- grounded answers with correct citations
- multi-document questions
- “must refuse” questions
- prompt injection attempts

### Failure tests you must run (Wave 1)
- simulate 429 throttling (model and gateway)
- simulate Search timeouts and partial failures
- verify retries/backoff and circuit breaker behavior
- verify refusal behavior when grounding is missing
- prompt injection attempts through uploaded documents

### Cost-aware performance testing
Load testing AI can be expensive.
- test realistic RPM with strict token caps
- measure tokens/request, not only latency
- run smaller targeted tests more often, full tests less frequently

**Trinity:** “What if latency is a bit high?”  
**Upendra:** “Then it’s a **No-Go**.”

Block release if:
- citation coverage drops
- cross-group retrieval is detected
- p95 latency breaches target
- tokens/request increases unexpectedly

---

## 13) GenAIOps change control (what must be versioned)

Version everything that can change behavior:
- `promptVersion`
- `indexVersion`
- `policyVersion`
- `modelDeploymentId`

Wave 1 release gates:
- golden test set pass
- security trimming tests pass
- injection tests pass
- rollback plan exists (prompt, model, index)

---

## 14) Responsible AI (minimum production controls)

Responsible AI is not a slide. It’s enforcement.

Wave 1 checklist:
- transparent citations on every grounded answer
- input and output content safety checks
- PII handling policy (refuse or redact)
- clear user disclosure (this is AI-generated)
- human escalation path for sensitive cases
- retention and right-to-be-forgotten process
- governance cadence for audits and policy reviews

---

## Scene 2: The Definition of Done

**Client Sponsor:** “So, what did we really ship?”

**Morpheus:** “A Copilot that doesn’t leak data, doesn’t collapse under load, and leaves an evidence trail for every answer.”

**Upendra:** “That is **Well-Architected AI**. The rest is just compute.”

---

## ✅ Launch Checklist (Wave 1)

**Architecture + security**
- [ ] Client calls **gateway only** (APIM)
- [ ] **Security trimming** enforced server-side
- [ ] No direct data-plane access (Search/OpenAI not reachable from UI)
- [ ] Private endpoints where required (Search, Storage)

**Quality + trust**
- [ ] **Evidence-or-refusal** enforced by validator
- [ ] Citation coverage tracked and gated
- [ ] “Must refuse” tests included in golden set

**Operations**
- [ ] Trace IDs end-to-end (`requestId`)
- [ ] Dashboards cover: p95 latency, 429 rate, refusal rate, queue depth, token/request
- [ ] Runbooks exist for throttling and ingestion backlogs

**Delivery discipline**
- [ ] IaC (Terraform) recreates the environment consistently
- [ ] Prompts, indexes, policies, model deployments are versioned
- [ ] Rollback plan exists and is tested

**Responsible AI**
- [ ] Content safety checks are active (in + out)
- [ ] PII policy enforced
- [ ] Audit governance cadence defined

---

## Bonus: WAF assessment cadence (how leaders keep it honest)

Run the Azure WAF AI assessment:
- once at design time
- once before go-live
- then every 4 months

Export recommendations and convert them into backlog work items. Track them like normal engineering work.

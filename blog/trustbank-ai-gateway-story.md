# Two Doors, One Rulebook: How TrustBank Scaled AI Agents Without Losing Control

TrustBank wanted **AI agents for customers** (internet-scale) and **AI agents for employees** (private-only). The CIO wanted speed. The CISO wanted an audit-proof control story. The solution was a **hybrid pattern** using **dual Azure API Management gateways (APIM)** with consistent “AI gateway” policies across both.

---

## What is an AI agent (simple)

An **AI agent** is an application that uses an AI model to understand a goal, decide steps, and call tools (APIs, search, ticketing, databases) to complete the task.

A chatbot mostly talks. An agent can **take actions**. That is why it needs stronger controls than a normal API.

---

## The cast

- **Cloud Architect (Neo):** architecture, standards, trade-offs  
- **Cloud Engineer (Trinity):** build, automation, operations  
- **Security Architect (Morpheus):** identity, data controls, audit requirements  
- **Firewall/Network SME:** routing, private DNS, egress control, no-bypass enforcement  
- **Migration Consultant:** onboarding waves, exception burn-down, legacy cutovers  
- **Project Manager:** decisions, RACI, milestones, reporting  
- **Customer Leadership (CIO/CISO/COO):** risk acceptance and operating model  

---

## The problem we had to stop

Before governance, teams tend to connect directly to:
- model endpoints (Azure OpenAI / Foundry Models), and
- tool APIs (search, DB, ticketing).

That creates three predictable failures:
1. **Uncontrolled cost** (token spikes).
2. **Inconsistent access control** (shadow integrations).
3. **Weak audit trail** (no single enforcement point).

The CISO requirement was clear:
> Controls must be enforced centrally, and we must be able to prove it.

---

## Architecture decision: Dual APIM (two doors)

We implemented **two separate APIM instances**:

- **APIM-External:** customer-facing agent APIs (internet entry via WAF/DDoS edge).
- **APIM-Internal:** employee-facing agent APIs (private-only via ER/VPN).

Both gateways implement the **AI gateway in APIM** capabilities (govern LLM endpoints and MCP/tool APIs).

### Reference diagram (simplified)

```text
External customers (Internet)
  -> Public Edge (WAF/DDoS)
  -> APIM-External (AI gateway policies)
  -> Private Model Endpoint (Azure OpenAI / Foundry)
  -> Private Tools/Data (Search, Storage, DB)

Internal employees (ER/VPN)
  -> APIM-Internal (private-only)
  -> Private Model Endpoint (Azure OpenAI / Foundry)
  -> Private Tools/Data (Search, Storage, DB)
```

### Network stance (defensible, not overclaimed)

- Model endpoints are configured for **private access** using **Private Endpoint + Private DNS**. Where required, public network access is disabled so Private Endpoint is the exclusive path.
- Tooling systems (for example, Azure AI Search) use the same private connectivity approach.
- **APIM-Internal** is deployed in **internal VNet mode** (or equivalent private-only access pattern), so it is reachable only within controlled networks.
- Egress is restricted so workloads cannot call model endpoints directly. Access is permitted only through approved gateway paths.

---

## “One rulebook” (the controls both gateways enforce)

This is the governance standard applied to both APIM instances:

1) **Identity** at the gateway (who is calling).  
2) **Request throttling** (requests per time window).  
3) **Token governance** (tokens per minute and/or token quotas) using APIM GenAI policies, including `azure-openai-token-limit`.  
4) **Audit-ready logging** with consistent fields and correlation IDs (caller, environment, model/deployment, tool invoked, token usage, latency, backend route).  
5) **Tool allowlisting** (agents can call only approved tools, not arbitrary URLs).  
6) **Exceptions** are time-boxed with an owner, expiry date, and compensating controls.

**Definition of done:** model and tool access is routed through controlled gateway paths with consistent policy and traceability.

---

## Day 1 scope (what we allowed, and what we did not)

### External customer agents (Phase 1)

**Allowed**
- Read-only knowledge and safe lookups (public FAQs, product guidance, status checks with strict scope).

**Not allowed**
- Any internal tools.
- High-risk actions (account changes, payments, entitlements).

### Internal employee agents (Phase 1)

**Allowed**
- Enterprise search and knowledge retrieval.
- CMDB and operational context lookups.
- Low-risk workflow actions (for example, ticket drafts or controlled ticket creation).

**Not allowed (until extra gates exist)**
- High-risk write actions without step-up controls (approval and/or human-in-the-loop).

---

## Four challenging scenarios, and how they were resolved

### Scenario 1: Bot storm and token cost spike (external)

**What happened:** a marketing event drove traffic. Bots piled in. Token spend threatened budgets.

**Controls**
- WAF bot controls at the edge.
- APIM-External enforced both request throttles and token budgets.
- Deterministic outcomes: `429` when rate limit hits, `403` when quota hits (based on token-limit policy behavior).

**Proof artifacts**
- Token usage by consumer, blocked calls, top callers (token metrics + gateway logs).

---

### Scenario 2: Prompt injection attempts and tool misuse

**What happened:** users tried “ignore instructions” prompts to extract internal data or trigger unsafe actions.

**Controls**
- External agent had no route to internal tools.
- Tool allowlist enforced at the gateway.
- Least-privilege identity per tool so an agent cannot exceed permissions even if prompted.

**Proof artifacts**
- Gateway logs show tool invocation only to approved tool APIs, with correlation IDs.

---

### Scenario 3: Model or region degradation

**What happened:** the primary model deployment slowed down during business hours.

**Controls**
- Multi-backend routing and defined failover behavior at the gateway.
- Degraded-mode responses for critical flows, so user experience fails safely rather than timing out.

**Proof artifacts**
- Backend route selection and failover events in logs, plus latency/error trends.

---

### Scenario 4: Legacy internal app could not move to modern auth quickly

**What happened:** a legacy ops system could not adopt the preferred identity approach in time.

**Controls**
- Time-boxed exception allowed only via APIM-Internal.
- Tight token quotas and enhanced logging.
- Compensating network controls (restrict egress paths, deny direct model access).

**Proof artifacts**
- Exception register with owner/expiry.
- Gateway logs validating constrained usage.

---

## Operating model (what CIO + CISO care about)

### Weekly KPIs

- % of model calls routed through gateways (target: as close to 100% as practical for production integrations)
- Token spend by app/team vs budget
- p95 latency and error rate per agent API
- Number of failovers and degraded-mode activations
- Exception count and burn-down trend

### RACI (one line each)

- **Accountable:** Cloud Architect for standards and design  
- **Responsible:** Cloud Engineer for build/run  
- **Consulted:** Security + Network SMEs for control enforcement  
- **Responsible/Consulted:** Migration Consultant for onboarding waves and removing exceptions  
- **Informed:** CIO/CISO/COO via KPI pack and risk register  

---

## Go-live checklist (use as gates)

- [ ] APIM-External and APIM-Internal deployed and scoped (clear separation of consumers)  
- [ ] Model endpoints private (Private Endpoint + private DNS), with public network access configured per policy  
- [ ] Tool services private (Search/DB/Storage) with required private DNS links  
- [ ] Gateway identity enforced  
- [ ] Request throttles + token quotas enabled  
- [ ] Token metrics enabled for monitoring  
- [ ] Tool allowlist implemented and least privilege validated  
- [ ] Failover tested (tabletop + practical drill)  
- [ ] Abuse tests executed (bot, quota, prompt injection)  
- [ ] Exceptions process live (owner, expiry, compensating controls)  

---

## Practical learning path (hands-on + videos)

### Hands-on labs and samples
- APIM ❤️ AI (Azure-Samples AI-Gateway repo): https://github.com/Azure-Samples/AI-Gateway  
- Token quota/rate limiting lesson (AI-Gateway docs): https://azure-samples.github.io/AI-Gateway/docs/azure-openai/rate-limit  
- Microsoft GenAI gateway reference architecture (APIM-based): https://learn.microsoft.com/en-us/ai/playbook/solutions/generative-ai/genai-gateway/reference-architectures/apim-based  

### Videos
- Securing and Scaling AI Workloads with AI Gateway in Azure API Management (YouTube): https://www.youtube.com/watch?v=gOopye0Hwo4  
- Connecting OpenAI Private Endpoints Across VNets (Microsoft show page): https://learn.microsoft.com/en-us/shows/azure-essentials-show/connecting-openai-private-endpoints-across-vnets  
- Governing AI Apps & Agents with AI Gateway in Azure API Management (Ignite lab session page): https://ignite.microsoft.com/en-US/sessions/LAB519  

---

## References (primary docs)

### AI gateway and APIM policies
- AI gateway in Azure API Management: https://learn.microsoft.com/en-us/azure/api-management/genai-gateway-capabilities  
- Limit Azure OpenAI API token usage (`azure-openai-token-limit`): https://learn.microsoft.com/en-us/azure/api-management/azure-openai-token-limit-policy  
- Emit token consumption metrics (`azure-openai-emit-token-metric`): https://learn.microsoft.com/en-us/azure/api-management/azure-openai-emit-token-metric-policy  
- APIM policies overview: https://learn.microsoft.com/en-us/azure/api-management/api-management-policies  

### APIM networking
- Deploy APIM to internal VNet (internal mode): https://learn.microsoft.com/en-us/azure/api-management/api-management-using-with-internal-vnet  
- APIM in internal mode behind Application Gateway (WAF): https://learn.microsoft.com/en-us/azure/api-management/api-management-howto-integrate-internal-vnet-appgateway  
- APIM virtual network concepts (options and trade-offs): https://learn.microsoft.com/en-us/azure/api-management/virtual-network-concepts  
- APIM inbound private endpoint: https://learn.microsoft.com/en-us/azure/api-management/private-endpoint  

### Private networking for AI services
- Secure Azure OpenAI inside a VNet with private endpoints: https://learn.microsoft.com/en-us/azure/ai-foundry/openai/how-to/network?view=foundry-classic  
- Private endpoint overview (Azure Private Link): https://learn.microsoft.com/en-us/azure/private-link/private-endpoint-overview  
- Create a private endpoint for Azure AI Search: https://learn.microsoft.com/en-us/azure/search/service-create-private-endpoint  

### Foundry configuration (optional)
- Configure AI Gateway in Foundry resources (associate APIM gateway): https://learn.microsoft.com/en-us/azure/ai-foundry/configuration/enable-ai-api-management-gateway-portal?view=foundry

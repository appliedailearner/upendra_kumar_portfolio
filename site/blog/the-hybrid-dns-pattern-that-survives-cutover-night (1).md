# The Hybrid DNS Pattern That Survives Cutover Night

Upendra Kumar  
January 2026  
Azure Networking. Private Link. DNS Governance.

Cutover night has a predictable failure mode.

The hub is up. The VPN is stable. The Private Endpoint is approved. Azure SQL has public access disabled. Everyone is ready to celebrate.

Then someone runs one command:

`nslookup azsql1.database.windows.net`

And the answer comes back public.

No outage banner. No firewall drop. No routing alarm.

Just DNS quietly sending your “private” traffic toward the public world.

This post documents the **Hybrid DNS pattern** we standardize on for UKLifeLabs-style landing zones. Central Private DNS zones in the hub. Azure DNS Private Resolver as the control plane. A design you can explain in 30 seconds and validate in 60.

---

## What we are solving

We want **on‑prem workloads** and **Azure spoke workloads** to resolve Azure PaaS service names to **Private Endpoint IPs**, without:

- DNS forwarder VM fleets
- split‑brain DNS zones across spokes
- manual record creation during migration waves
- last‑minute fixes on cutover night

**Non‑negotiable rule:**  
If the service is private, the name must always resolve to a private IP.

---

## Challenge: DNS ownership breaks private endpoint designs

The most common failure is not networking. It is ownership.

When every team creates its own Private DNS zones, you get:

- inconsistent records
- partial resolution depending on where the query originates
- outages that only appear during cutover

**Key takeaway:** Private Endpoints are a network feature, but DNS is an operating‑model decision.

---

## Decision 1: Centralize Private DNS zones in the Hub

All Private DNS zones live in the **Hub (Connectivity)** subscription or resource group.

Example:
- `privatelink.database.windows.net`

Why this works:
- single source of truth
- simple governance story
- predictable behavior across all spokes

**Rule:** One zone per service. Never one zone per team.

---

## Decision 2: Use Azure DNS Private Resolver (no DNS VMs)

We deliberately avoid DNS forwarder VMs.

Instead we use:
- **Azure DNS Private Resolver**
- **Inbound endpoint** for on‑prem → Azure queries
- Optional **Outbound endpoint** for Azure → on‑prem resolution

Benefits:
- managed service
- no patching
- no custom HA design
- built for hub‑and‑spoke scale

**Key takeaway:** DNS should not be a custom VM workload.

---

## Target architecture

**Topology:** On‑prem → Hub → Spoke

### Hub (Connectivity)
- Azure DNS Private Resolver  
  - Inbound endpoint (example: `10.10.0.4`)
- Central Private DNS zone  
  - `privatelink.database.windows.net`
- VNet links to spokes that require resolution

### Spoke (Workload)
- Azure SQL Server (public access disabled)
- Private Endpoint `pe-sql` (example: `10.20.1.4`)
- Private DNS zone group linked to the hub zone

---

## Workflow (cutover‑safe resolution path)

1. Client queries `azsql1.database.windows.net` via on‑prem DNS  
2. On‑prem DNS conditionally forwards `database.windows.net` to Resolver inbound endpoint  
3. Inbound endpoint hands query to DNS Private Resolver  
4. Resolver determines Private Link CNAME  
5. Resolver queries `privatelink.database.windows.net`  
6. Private DNS zone returns Private Endpoint IP  
7. Resolver returns answer to on‑prem DNS  
8. On‑prem DNS returns private IP to client  
9. Client connects privately to Azure SQL via Private Endpoint

**Result:** Same name. Private IP. Private path.

---

## Why this survives cutover night

- Central DNS governance
- Predictable resolution chain
- No hidden DNS VMs
- One place to validate and troubleshoot

---

## Common failure modes

- Forwarding `privatelink.*` instead of public suffix
- Private DNS zone not linked to the required VNet
- Private Endpoint missing DNS zone group
- NSGs blocking UDP/TCP 53 to inbound endpoint

---

## 60‑second validation test

From on‑prem:

`nslookup azsql1.database.windows.net`

Expected:
- Private Endpoint IP

If you get a public IP, DNS is broken.

---

## Operating model

**Platform team**
- DNS Private Resolver
- Private DNS zones
- VNet links
- Policy and guardrails

**Application teams**
- Private Endpoints
- Request or attach DNS zone groups

---

## Reference implementation

A working Terraform‑based reference implementation is available here:

https://github.com/appliedailearner/privatednsresolver/tree/main

---

## Closing thought

Private Link is not the hard part.

Making DNS boring is.

This pattern does exactly that.

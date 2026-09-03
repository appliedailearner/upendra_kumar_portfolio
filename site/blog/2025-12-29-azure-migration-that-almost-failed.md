---
title: "The Azure Migration That Almost Failed. Until We Fixed Ownership, Decisions, and Guardrails"
author: Upendra Kumar
section: insights
tags:
  - Azure Migration
  - Azure Landing Zone
  - Cloud Architecture
  - Enterprise Architecture
summary: >
  A real-world Azure migration story showing how DRIs, RFCs, and guardrails transformed a stalled landing zone program into a scalable execution model.
---

# The Azure Migration That Almost Failed. Until We Fixed Ownership, Decisions, and Guardrails

## Act 1: The Illusion of Progress

It started like most enterprise cloud initiatives: high energy, a mandate from the CIO, and two senior engineers—myself and a lead from the partner SI—staring at a whiteboard. We had the "perfect" plan. We had the Microsoft Cloud Adoption Framework (CAF) diagrams printed out. We had a backlog of 400 VMs to move.

For the first three months, we felt productive. We deployed a Hub-and-Spoke network. We built a few management groups. We even migrated a couple of low-risk dev workloads. The status reports were green.

But we were building a facade.

Underneath the Terraform scripts and the weekly standups, we didn't have an operating model. We had two people making every single decision in a vacuum. We were the bottleneck, the escalation point, and the execution team all at once. We just didn't know it yet.

## Act 2: The Silent Killer (Missing Decision Mechanics)

The cracks appeared when we tried to scale. The application teams started asking questions we hadn't anticipated:
*   "How do we handle private endpoint DNS resolution for our PaaS services?"
*   "Who approves the firewall rules for the new subnet?"
*   "Why can't we use the standard marketplace image for our legacy app?"

Every question triggered a meeting. Every meeting triggered an email chain. Every email chain waited for me or the other lead to say "yes" or "no."

We weren't doing architecture anymore; we were doing traffic control for a traffic jam we had created. The problem wasn't technical. The problem was that we lacked a **decision mechanic**. We treated architecture as a static deliverable, not a dynamic process of trade-offs.

## Act 3: The Cutover That Wasn't

The breaking point came on a Tuesday night. We were scheduled to cut over a critical financial reporting application. The "Migration Factory" (a team of 5 contractors) had moved the bits. The database was syncing.

At 2:00 AM, we called a rollback.

The application couldn't talk to the on-prem mainframe. Why? Because the route table (UDR) on the spoke subnet was missing a specific next-hop to the NVA, and the firewall rules hadn't been propagated to the secondary region's policy. Worse, the application relied on a hardcoded IP that changed during the move, and we had no internal DNS resolution for the new private endpoint.

It was a humiliating failure. It wasn't a "glitch." It was a systemic failure of our landing zone to support the actual workload requirements.

## Act 4: Introducing DRIs (Directly Responsible Individuals)

We paused the migration for two weeks. I knew we couldn't just "try harder." We needed to change how we worked.

The first step was establishing **DRIs (Directly Responsible Individuals)**.

We stopped being the "Cloud Team" and started breaking down ownership.
*   **Identity DRI:** Owned Entra ID, RBAC, and PIM.
*   **Network DRI:** Owned the Hub, Firewalls, ExpressRoute, and DNS.
*   **Security DRI:** Owned Azure Policy and Defender for Cloud.

I moved from being the person *doing* everything to the person *orchestrating* the DRIs. If a firewall port needed opening, the Network DRI owned the decision, the implementation, and the risk.

## Act 5: The RFC Revolution

Next, we killed the "meeting to decide" culture. We implemented a strict **Request for Comments (RFC)** process.

If you wanted to deviate from the standard pattern—say, use a Public IP instead of a Private Endpoint—you didn't schedule a meeting. You wrote a 2-page Markdown document:
1.  **Context:** What are you trying to do?
2.  **Options:** What are the alternatives (A, B, C)?
3.  **Recommendation:** Why is B the right choice?
4.  **Trade-offs:** What risks are we accepting?

We reviewed these asynchronously. Decisions were logged. We stopped re-litigating the same arguments every week. The velocity of decision-making tripled because we forced clarity before conversation.

## Act 6: Guardrails as Enablers

With ownership and decisions fixed, we tackled the fear of breaking things. We shifted from "gatekeeping" to "guardrails."

We implemented **Azure Policy** in "Deny" mode for the non-negotiables:
*   No Public IPs on NICs.
*   No unencrypted storage accounts.
*   Allowed regions only (East US 2 / Central US).

For everything else, we used "Audit." This gave the migration factory confidence. They knew that if the deployment succeeded, it was compliant. They didn't need to ask for permission; the platform gave them permission by not failing.

## Act 7: The Portfolio Assessment Backbone

We revisited our backlog. The initial "list of VMs" was useless. We needed a **Portfolio Assessment**.

We enriched our inventory with metadata that actually mattered for migration:
*   **Dependency Map:** What talks to what? (We used Azure Migrate dependency visualization).
*   **Business Criticality:** Is this a Tier 1 app or a Tier 3 tool?
*   **Data Classification:** PII/PCI?

This allowed us to group applications into "Move Groups" based on affinity, not just alphabet. We stopped trying to move "servers" and started moving "capabilities."

## Act 8: Right-Sizing and the Business Case

We also got serious about money. The "lift and shift" was projected to increase costs by 20%.

We implemented an aggressive **Right-Sizing** framework. We didn't just look at allocated CPU; we looked at *consumed* CPU (95th percentile) over 30 days.
*   On-prem: 8 vCPU, 32GB RAM (Allocated)
*   Usage: 5% avg, 15% peak
*   Azure Target: Standard_D2s_v5 (2 vCPU, 8GB RAM)

We combined this with Azure Hybrid Benefit (AHB) and 3-year Reserved Instances. Suddenly, the business case flipped from a 20% increase to a 15% savings. The CFO became our biggest advocate.

## Act 9: From Heroics to Runbooks

Finally, we codified the execution. We banned "heroics."

We built a **Migration Runbook** that was boringly detailed.
*   T-minus 4 weeks: Enable replication.
*   T-minus 1 week: Pre-cutover validation (DNS, Firewall).
*   T-minus 2 hours: Stop app services.
*   T-minus 0: Final sync and cutover.

We created checklists for everything. If it wasn't on the checklist, it didn't happen. The excitement of the migration night vanished. It became a boring, predictable series of checkboxes. And that is exactly what enterprise architecture should be.

## Lessons Learned

We didn't succeed because we wrote better Bicep code. We succeeded because we treated the migration as a **product**, not a project.

1.  **Architecture is political.** You must define who owns the decision, or no decision gets made.
2.  **Guardrails enable speed.** Safety brakes allow you to drive faster, not slower.
3.  **Boring is better.** Predictable runbooks beat heroic troubleshooting every time.

If you are stuck in a migration that feels like it's moving through mud, stop looking at the technology. Look at your decision mechanics.

---

### Ready to operationalize your Azure journey?

I help organizations turn stalled cloud initiatives into execution engines.

[**Contact Me**](/contact.html){: .btn .btn-primary } [**View the Toolkit**](/pages/azure-migration-toolkit.html){: .btn .btn-outline }

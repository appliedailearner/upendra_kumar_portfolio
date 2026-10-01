# Changelog: SecOps post revision (30 September 2026)

- **Post A (revised):** `site/blog/2026-09-28-unified-security-operations-ai-era.html`, now titled "Minutes vs. Months: Closing the SOC Gap in the Age of AI Agents". It is for CISOs and CIOs.
- **Post B (new):** `site/blog/2026-09-30-microsoft-security-partner-playbook.html`, titled "The Microsoft Security Partner Playbook: Turning the SOC Gap into a Services Practice". It is for Microsoft partners.
- **Also updated:** `site/blog.html` (the Post A card and a new Post B card), `site/feed.xml` and `site/sitemap.xml`.
- **Status (1 Oct 2026):** the owner approved both posts. All `VERIFY` and `CONFIRM PUBLIC` HTML comments were removed from both pages so nothing leaks via the page source; this changelog is now the only record of them. Not yet deployed.

---

## Fixes

### A. Accuracy and currency

| # | What changed |
|---|---|
| A1 | **Title and hook reframed.** The new framing is the attacker's clock (minutes) against the defender's clock (months). The page now says outright that these are two different measurements. The `<title>`, meta description, `og:`/`twitter:` tags, JSON-LD headline, blog card and RSS item all carry the new title: "Minutes vs. Months: Closing the SOC Gap in the Age of AI Agents". The description reads "Attackers move in minutes; the average breach takes 247 days to contain…". |
| A1 (data) | **Breach figures updated.** 292 days (IBM 2024, stolen-credential breaches) is replaced by **247 days** (IBM Cost of a Data Breach 2026: 183 days to identify plus 64 to contain). The 292 figure is dropped entirely rather than kept as a historical label, because the post no longer needs it. |
| A2 | **Conclusion rewritten.** The claim "transforms 292-day containment timelines into 20-minute response" is gone. It now says: containment in minutes "on the attack paths you've onboarded", plus IBM 2026's finding that heavy use of security AI and automation cut the breach lifecycle by 65 days. It adds: "What I won't claim is that a licence does it on its own." |
| A3 | **72 minutes** is now attributed to the **Microsoft Digital Defense Report 2022** ("once they are clicked on the average time for an attacker to access private data is 1 hour and 12 minutes"). **67% AI phishing:** no primary source was found, so the figure is removed and a VERIFY comment explains why. In its place are figures I confirmed from MDDR 2025: more than 97% of identity attacks are password attacks, and MFA blocks over 99% of identity-based attacks. |
| A3 (extra) | **Other stat tiles.** The 66% (identity) and 84% (internet exposure) attack-path tiles had the same unconfirmed "Microsoft threat intelligence" attribution, so they are removed and marked VERIFY. That also removes "two-thirds of attack paths run through identity" from the executive summary and the roadmap. The 73% alert figure is now attributed to the **Coro SME Security Workload Impact Report 2024** (500 US security decision-makers at SMEs). |
| A4 | **Case studies reconciled.** The section is renamed **"Attack Disruption: Contained in Minutes"**. Both incidents now use one measure, *click to containment*: case 1 is 10 minutes (T+10m to T+20m, or 20 minutes from email delivery), and case 2 is 17 minutes (T+234m to T+251m). The "12 vs 11" point was not actually a contradiction: the campaign was disrupted for **12 users across 11 other organisations**. The step and the caption now say exactly that. The case details come from partner materials, so they are marked VERIFY (see V4). |
| A5 | **Security Copilot's E5/E7 inclusion** (MC1478465) now appears in two places: the CFO slide section, with the 400 SCUs per 1,000 users capped at 10,000, the agent experiences it covers and what still costs extra; and the Days 90–180 "Close the loop" step. |
| A6 | **Days 30–90, "Single portal".** Now reads: "Act now: managing Sentinel in the Azure portal ends on **31 March 2027**." |
| A7 | **Defender Experts.** The Forrester TEI (July 2023) is now labelled "**dated**: a projection, not a measured result". The researcher figure is confirmed as "more than 10,000 security researchers" (Microsoft Security blog, 10 August 2026). The page now uses the current name, **Defender Experts MDR** (renamed from Defender Experts for XDR, July 2026). The old "80+ billion signals a day" line is dropped; Microsoft now says 100 trillion. The four-tile Forrester block is reduced to one sentence to save reading time. |

### B. Architecture depth

| # | What changed |
|---|---|
| B8 | **Agent identity.** A new subsection, "Every agent needs its own identity", covers Entra Agent ID (generally available), a named sponsor and a lifecycle for each agent, and Conditional Access and ID Protection for agents (Agent 365 or Microsoft 365 E7, MC1395007). It also notes the agent registry converging into Agent 365. Design principle 1 is now "Zero Trust identity for humans, workloads and agents". The threat table's Initial access and Credential theft rows now list Agent ID and ID Protection for agents. |
| B9 | **MCP servers.** A new subsection, "Treat MCP servers as privileged integrations", covers three controls: register and allow-list through API Management as the AI gateway; least privilege per tool call; and screening tool outputs with Prompt Shields for indirect prompt injection. The table has a new row, "Malicious tool and MCP use", and the diagram shows the API Management box with "MCP allow-list". |
| B10 | **New "Framework" column.** OWASP IDs are checked against genai.owasp.org (2025 list). MITRE ATLAS IDs are checked against the ATLAS data file v5.6.0. The mapping per row: **Prompt injection:** LLM01:2025; AML.T0051 (.000 direct, .001 indirect), AML.T0054. **Initial access:** AML.T0012 Valid Accounts, AML.T0052 Phishing, AML.T0049 Exploit Public-Facing Application; there is no direct OWASP LLM entry, and the table says so. **Tool/MCP:** LLM06:2025, LLM03:2025; AML.T0053 AI Agent Tool Invocation, AML.T0110 AI Agent Tool Poisoning. **Credential theft:** LLM02:2025; AML.T0055, AML.T0083, AML.T0098. **Lateral movement:** LLM06:2025; AML.T0091. **Exfiltration:** LLM02:2025; AML.T0057, AML.T0086. |
| B11 | **Non-Microsoft signals.** A new subsection, "It doesn't have to be a Microsoft-only SOC", covers AWS CloudTrail and GuardDuty, Google Cloud audit logs, CEF/Syslog firewalls, SaaS and OT through Sentinel connectors; the Sentinel data lake for high-volume sources; and Defender Experts MDR Plan 2 coverage of non-Microsoft sources. The reference diagram shows the same inputs. |
| B12 | **Ingestion caveat made concrete.** Analytics tier: Entra ID sign-ins, EDR and email alerts, where rules run. Data lake tier: firewall or NetFlow logs kept a year for forensics, which is cheaper but runs no analytics rules. This follows Microsoft Learn's guidance on which logs to send to the data lake. |

### C. Commercial honesty

| # | What changed |
|---|---|
| C13 | **Price caveat moved.** A "Read this before you show the slide" box now sits directly under the price table and arithmetic. It says Business Premium already includes Defender for Business and Entra ID P1, so the standalone column overstates the gain, and that $54,600 and $96,600 are the gap to list prices, not savings. The old caveats bullet ("The price table is for Business Premium") is merged into it. |
| C14 | **New table: "Measure it: four SOC outcome metrics".** It covers mean time to detect, mean time to respond, alerts per analyst per shift, and incidents closed by automation, with 90-day and 180-day example targets. It is labelled "Example targets, not benchmarks or claims". The baseline column became a caption ("measure your baseline in days 0–30") to save space. |
| C15 | **New section: "Objections You'll Hear".** It has three answers. The "What if Microsoft is breached?" answer links to the existing Secure Future Initiative box, which now has `id="trust"`. |
| C16 | **New note for Indian readers.** DPDP Rules were notified in November 2025, with most obligations (including breach notification and cross-border transfers) applying from May 2027. It covers the negative-list transfer model, sector regulators such as RBI, and possible localisation for significant data fiduciaries. |

### D. Story and structure

| # | What changed |
|---|---|
| D17 | **Post split in two.** Post A keeps the executive summary, hook, six consoles, attack disruption, AI attack surface, reference architecture, finance case (CFO slide, 24/7 cover, metrics, trust), roadmap, caveats, objections and conclusion. "From Reactive to Predictive" and the standalone "24/7" section are folded in or cut, because they weren't in your Post A outline. **Post B** holds the partner material: solution plays, the Forrester 2025 growth data, four dated conversation starters (Sentinel deadline, Copilot in E5/E7, agent identity, IBM 2026), the win formula, funding and designation (public-safe text only) and delivery. **FY:** Post B says FY27 began 1 July 2026. The solution plays are labelled "as published for FY26" with a VERIFY for their FY27 names. The posts link to each other: Post A's author note links to Post B, and Post B links to Post A three times (author note, `#economics`, `#roadmap`). |
| D18 | **The 9:00 finance employee.** They open the post as before. They return in "Back to 9:00 in finance", where their click is replayed minute by minute on case 1's timings (labelled illustrative). They close the conclusion: "the click at 9:00 is a risky sign-in at 9:01 and a disabled account at 9:10…" |
| D19 | **Repetition removed.** The executive summary states the problem, play and ROI once. The conclusion no longer restates them: it gives the board-defensible claim, the finance story and the next step. |

### E. Visuals, SEO and call to action

| # | What changed |
|---|---|
| E20a | **Inline SVG: before and after.** Six consoles and queues become one signal plane (Defender XDR, Sentinel, Security Copilot). It has `<title>` and `<desc>` and `role="img"` with `aria-labelledby`. |
| E20b | **Inline SVG: layered reference architecture.** The layers are Edge & Access (Front Door + WAF, API Management with MCP allow-list, Entra ID + Agent ID), AI Platform, Posture & Data Signals and the Unified SecOps Plane, plus a non-Microsoft signal input. It replaces the HTML box diagram. |
| E20c | **Inline SVG: 9:00 timeline.** A horizontal strip from 8:50 to 9:10, bracketed "10 minutes, click to containment". |
| E20 (theme) | **Dark and light mode.** All three diagrams draw their own panel. The colours are CSS classes in the post's own `<style>`: a dark palette by default, and a light palette under `@media (prefers-color-scheme: light)`. The site itself has no light theme. |
| E21 | **Canonical link, JSON-LD and date line.** Added `<link rel="canonical">`. The JSON-LD has the new headline and description, `datePublished` 2026-09-28, `dateModified` 2026-09-30 and the existing og image. The hero shows "Last updated September 30, 2026". Post B has the same set, dated 2026-09-30. |
| E22 | **New call to action.** "Ready to operationalize your Azure journey?" and "View the Toolkit" are replaced by **"Book a SOC Consolidation Readiness Check"**, with a primary button to the contact page, a secondary "Get the 180-day plan" (goes to `#roadmap`) and a "Contact me" link. |

### F. Held for your approval

- No NDA-sensitive partner detail is in Post B's visible text.
- The five items are in a `<!-- CONFIRM PUBLIC BEFORE PUBLISHING -->` comment inside Post B's "Funding and Designation" section (listed below).

---

## VERIFY items

`VERIFY` comments are in the page source. Items without a marker in the HTML are flagged here only.

| # | Claim | Where | Suggested source to check |
|---|---|---|---|
| V1 | "67% of phishing attacks used some form of AI" (removed from page) | Post A, Two Clocks (comment) | The Microsoft Digital Defense Report 2025 full PDF; the original partner deck's footnote |
| V2 | "66% of attack paths involve identity" and "84% involve an internet exposure" (removed) | Post A, Two Clocks (comment) | Microsoft Security Exposure Management data as cited in MDDR 2024/2025; the partner deck footnote |
| V3 | Five Secure Future Initiative figures (95% video ID verification, 5.75M tenants, 99.3% network assets, 85% pipelines, 90% vulnerabilities). They are removed from the page because they mix reports; the April 2025 report says 6.3M tenants and 73% | Post A, `#trust` box (comment) | The SFI progress report, July 2026 edition; cite the edition for each figure |
| V4 | Case 1 (financial services, Jan 2025) and case 2 (C-suite testimonial) timelines | Post A, disruption section (comment) | Microsoft Security blog or customer story for each incident |
| V5 | CSP list prices in the price table (FY26) | Post A, CFO slide (comment) | The current FY27 CSP price list or Microsoft 365 Business Premium add-on pricing |
| V6 | Microsoft 365 licence data grant for Sentinel ingestion (no number quoted) | Post A, objections (comment) | The Microsoft Sentinel pricing page and the Microsoft 365 E5 benefit terms |
| V7 | DPDP: exact commencement date (13 or 14 May 2027); whether data has been specified for localisation by significant data fiduciaries (Rule 13) | Post A, India note (comment) | The Gazette notification G.S.R. 846(E) and MeitY notices |
| V8 | Agent 365 generally available 1 May 2026 | Post A, agent identity (comment) | Microsoft 365 licensing documentation (currently sourced to a Tech Community post) |
| V9 | FY27 names for the three security solution plays and hero products | Post B, Three Solution Plays (comment) | FY27 Microsoft partner solution-play guidance (Partner Center) |
| V10 | IBM 2026 "247 days" and "phishing top vector, fourth year". The IBM-linked summary returned 403 to me; I confirmed the figures via other summaries (Security Boulevard, databreachcost.com) | Post A (no HTML marker) | The IBM report PDF (ibm.com/reports/data-breach) |
| V11 | 72 minutes is a **2022** Microsoft figure; newer MDDR editions may not repeat it | Post A (no HTML marker; the year is shown on the page) | MDDR 2024 and 2025, to see whether a newer median exists |

## CONFIRM PUBLIC items (Post B, HTML comment, not visible on the page)

| # | Claim | Where it would go | Check |
|---|---|---|---|
| P1 | Immersion briefings are 90-minute, 1:many sessions for 5–25 eligible customers | Post B, Funding and Designation | Whether the FY27 partner incentives guide is public |
| P2 | Immersion funding of up to $2K per briefing (FY26) for partners with the Security Solution Partner Designation for SMB | Same | The same guide |
| P3 | Designation scoring: 100 points (performance 20, skilling 40, usage growth 20, deployments 20), 70 required | Same | The public Partner Center designation page |
| P4 | "Structural CSP incentives apply" at the win stage | Same | The CSP incentives guide |
| P5 | Security Business Case Builder "upgraded May 2025, grounded in Forrester TEI data" | Same (Post B mentions the tool by name only) | The partner tool page |

**Important:** HTML comments are visible to anyone who views the page source. The `CONFIRM PUBLIC` block, and ideally the `VERIFY` comments too, must be deleted before either page is deployed.

---

## Reading time

The site's existing figure ("18 min") works out to 200 words a minute on the full article text. I used the same rate.

| | Before | After |
|---|---|---|
| Post A, article text excluding the Contents and Sources lists | 3,427 words, about 17.1 min | **2,393 words, about 12.0 min** (shown as "12 min read") |
| Post A, everything including those two lists | 3,596 words, 18.0 min | 2,642 words, 13.2 min |
| Post A, diagram labels (not counted above) | none | 189 words |
| Post B, article text excluding lists | n/a | 777 words, about 4 min |

---

## Self-check

- **No number without a source.** I listed every number in the visible text of both posts. Each one is one of these:
  - attributed inline to a named report and year (IBM 2026, MDDR 2022/2025, Coro 2024, Forrester 2023/2025, Microsoft Security blog July/August 2026) or a message-center ID (MC1478465, MC1395007);
  - a product or date fact listed in Sources (31 March 2027, DPDP dates);
  - a CSP price cited as "Microsoft Security partner materials (FY26)", marked VERIFY;
  - explicitly illustrative (the 9:00 replay, the 4,000-file example, the example metric targets, the 250-seat and 5,000-seat scenarios).

  The lead's 72 minutes and 247 days have a source caption directly under the lead.
- **Price table maths reconciles.**
  - Standalone sums: $5.20 + $5.00 + $5.50 + $3.50 + $9.00 = **$28.20**; adding $6 + $6 + $7 gives **$47.20**.
  - Savings: 250 × ($28.20 − $10.00) × 12 = **$54,600**; 250 × ($47.20 − $15.00) × 12 = **$96,600**.
  - Deltas: 64.5% (shown as ~65%) and 68.2% (shown as ~68%).
- **SVGs readable in dark mode.**
  - I took screenshots at 1440px (dark and light) and 390px (dark). No label overlaps or overflows after fixing the timeline and architecture labels.
  - Dark-mode text contrast: `#f1f5f9` on `#1e293b` is about 13:1; `#cbd5e1` on `#1e293b` is about 10:1; `#94a3b8` on `#0b1222` is about 7:1.
  - No sideways page scroll at 390px.
  - **Limitation:** on a 390px phone the smallest diagram labels scale to about 8 CSS px. They are legible on high-density screens but smaller than body text. The audit's T09 check skips SVG text, so it won't flag this.
- **All internal links resolve.**
  - Post A: 24 internal links and anchors.
  - Post B: 19, including the cross-post anchors `#economics` and `#roadmap`.
  - `blog.html`: 5 links for the two cards.
  - I checked all of these with a script against the files and their `id`s.
- **Site audit (`blog-visual-audit.js`, 21 checks, desktop and phone).** Both posts pass. Only the informational phone paragraph-length warning remains.

## Before publishing

1. Resolve or accept each VERIFY item, and confirm or drop P1–P5.
2. Delete the `CONFIRM PUBLIC` comment block (and the VERIFY comments) from the HTML.
3. Re-run `node tools/qa/blog-visual-audit.js <post>` for both posts. Then commit, push, run the Azure deploy and the `--live` audit.

---

## Audit round 2 (1 October 2026)

An expert review of both live posts found 19 issues. All of them are fixed except #13 and #16, which stay open.

| # | Fix |
|---|---|
| 1 | **New share images.** Each post has its own: `images/blog/2026-09-28-minutes-vs-months-og.webp` and `2026-09-30-partner-playbook-og.webp`. The old image still said "72 minutes vs 292 days". New script: `tools/scripts/make-og-image.js <config.json>`. |
| 2 | **EDR objection now states the trade-off.** Automatic disruption contains devices and users only through Defender for Endpoint, so a third-party EDR loses cross-domain containment. |
| 3 | **IBM finding reworded as a comparison, not a cause.** It now reads "organisations using security AI and automation extensively had lifecycles 65 days shorter and costs $1.93M lower", in the executive summary, the conclusion and the sources list. |
| 4 | **9:09 honesty line.** The attacker still opened a file before containment: disruption shrinks the blast radius, it doesn't promise zero access. |
| 5 | **72 minutes.** "median" removed from the stat tile and sources; the 2022 report's wording is unconfirmed. |
| 6 | **MFA figure.** Now "over 99% of identity-based attacks", not "of them". |
| 7 | **Timeline 9:08.** Now "Phishing email auto-removed", not "pulled everywhere". |
| 8 | **Copilot allowance.** New line: agents draw on it continuously, so measure a month of use first. |
| 9 | **Roadmap Days 0–30.** Adds Defender for Identity sensors on domain controllers, which disabling on-premises accounts requires. |
| 10 | **Design principle 2.** Now "Private networking and controlled egress", with an allow-listed outbound path (Azure Firewall or a network security perimeter). |
| 11 | **Two new threat-table rows.** "Grounding data poisoning" (OWASP LLM04/LLM08; ATLAS AML.T0070 RAG Poisoning) and "Runaway consumption" (LLM10; ATLAS AML.T0034 Cost Harvesting), each with its controls. |
| 12 | **Lock-in answer.** Attack disruption now acts on Okta users and AWS IAM through Sentinel (preview), per Microsoft Learn. |
| 13 | **OPEN:** the Forrester partner figure "versus 23% overall growth" is still ambiguous; confirm against the study (now **V12**). |
| 14 | **Post B offer map.** New table: phase, offer, commercial model (fixed fee or recurring). |
| 15 | **Post B certifications.** Names public paths: SC-200, SC-100 and SC-401, linked to Microsoft Learn. |
| 16 | **OPEN:** V9 (FY27 solution-play names) and P1–P5 are unchanged. |
| 17 | **Search snippets.** Post A's description cut to 152 characters (meta, og, twitter, JSON-LD, listing, feed). `<title>` shortened on both posts. |
| 18 | **Leftover script removed.** Post A's per-post contents-tracker script is gone (`js/toc-tracker.js` handles it). |
| 19 | **Sources linked.** Adds links to IBM 2026, MDDR 2022, the Forrester Defender Experts TEI PDF, API Management token limits and network security perimeter. |
| extra | **Forrester ROI range.** The study's 254% is its high-impact scenario only. The page now gives the full range: 43% (low) to 254% (high), with 147% as medium. |
| extra | **Stale airport reference.** It was left after the analogy was cut and is now removed ("the six-console problem again"). |

**Post A's licensing note was removed.** The onboarding step and the EDR objection now cover it.

**Reading time:**
- Post A: 2,398 words, 12.0 minutes (same method: 200 wpm, excluding the Contents and Sources lists).
- Post B: 885 words, 4.4 minutes (shown as "4 min read").

**Checks:** both posts pass all 21 audit checks locally. All internal links resolve, and the three SVGs were re-checked in dark and light mode at desktop and phone widths.

---

## Open items closed (1 October 2026)

| Item | Finding | What changed on the page |
|---|---|---|
| **V12** Forrester partner figures | **The page's figures were wrong.** Forrester's *The Partner Opportunity For Microsoft Security Partners* (November 2025, commissioned by Microsoft) models expected revenue from **one new enterprise customer**, based on 15 partner interviews. The model grew 20% year on year. Managed services is the largest stream ($23.35 of $54.35 per user per month) and grew 24%; advisory grew fastest at 35%. **There is no SMB cohort.** The "42%" in the study is the blended attach rate, not a growth figure. The July 2024 edition shows SMB managed services +53% and enterprise +17%; it doesn't support 42/23 either. | Post B, "Where the Growth Is", was rewritten with the November 2025 figures and their caveats, and the source is linked. The "SMB 42% vs 23%" claim is removed. "The growth is in managed services" is corrected to: managed services is the largest stream, advisory the fastest-growing. |
| **V9** FY27 solution plays | Microsoft's public Security Partners site lists the FY27 plays: **Establish a trusted & secure platform for AI** (enterprise; Microsoft 365 E7, Agent 365), **AI-ready productivity & security for every employee** (enterprise; Copilot, Microsoft 365 security) and **Run your Business Securely** (SMB; Business Premium). The FY26 play names are no longer listed there. | Post B's play table is replaced with the FY27 plays and featured products. A caption notes the FY26 names. |
| **P1** Immersion briefings | Public in Microsoft partner news: 90-minute partner-led briefings for SMB customers on three topics (Threat Protection, Data Security, Advanced Security for Business Premium). Partners can claim co-op funding for delivery costs and have up to 20 submissions open at a time. **"5–25 customers" was not found in any public source.** | Published, without the customer count. |
| **P2** "$2K per briefing" | Not found in any public source. | **Not published.** The page says to check amounts in Partner Center. |
| **P3** Designation scoring | **Public on Microsoft Learn.** The minimum is 70 of 100 points, with at least 1 point in each of four metrics: net customer adds, intermediate certifications, deployments and usage growth. Net customer adds, deployments and usage growth are each capped at 20. There are SMB and enterprise paths, and the better score counts. The required certifications: Azure Security Engineer (retired 31 Aug 2026) or Cloud and AI Security Engineer, plus SC-200; points then come from SC-100, SC-300 or SC-401. **The old deck's "performance 20, skilling 40, usage 20, deployments 20" matched in total, but "deployments" is a customer-success metric.** | Published with the Learn link. The certification guidance now follows the designation's actual required path. |
| **P4** CSP incentive details | Only third-party summaries were found. | **Not published.** The step stays generic ("check the current program guide"). |
| **P5** Business Case Builder "upgraded May 2025" | Not verified. | **Not published.** The tool is named only. |
| **V4** Case-study incidents | No public Microsoft case study was found for either incident. | Attributed honestly: "Two incidents from Microsoft partner materials (FY26; not public case studies)". |
| **V5** Prices | Suite prices ($10 and $15) are confirmed on Microsoft's SMB security add-on pricing page. The $47.20 standalone total matches independent breakdowns. | Price line re-sourced and the pricing page linked. Component prices are still attributed to partner materials. |
| **V6** Sentinel data grant | Confirmed: Microsoft 365 E5, E7, A5, F5 and G5 include up to 5 MB per user per day of Microsoft 365 data ingested into Sentinel (Azure offer page). | The ingestion-cost objection now states it, with a link. |
| **V8** Agent 365 GA | Confirmed by the Microsoft Security blog, 1 May 2026. | The Tech Community source is replaced. |

**Closed 1 October 2026:**
- **V7:** DPDP obligations apply from 13 May 2027, 18 months after the Rules were notified on 13 November 2025 (Legal500, PrivacyWorld). The page now gives the exact date.
- **V10:** IBM 247 days = 183 to identify + 64 to contain. Help Net Security, HIPAA Journal and Security Boulevard all report it the same way; IBM's landing page shows only the cost figures. The source list now gives the split and links Help Net Security.
- **V11:** Microsoft's MDDR 2022 gives a **median** of 1 hour 12 minutes. The source list now says so; the body keeps "about 72 minutes".

**Still off the page:**
- **V1–V3:** figures that were removed from the page and stay off.

**Reading time:**
- Post A: 2,400 words, 12.0 minutes.
- Post B: 1,032 words, 5.2 minutes (shown as "5 min read" on the post and in the listing).

**Checks:** both posts pass all 21 audit checks, and all internal links resolve.

## New figure: unified SecOps loop (1 October 2026)

- **What:** a fourth inline SVG (`dgD`) in Post A, placed after the Okta / AWS IAM / Defender Experts MDR paragraph in "It doesn't have to be a Microsoft-only SOC". It shows Microsoft signals going natively into Defender XDR and non-Microsoft signals going through Sentinel connectors, one unified SecOps plane (Defender XDR, Security Copilot, Sentinel) producing one incident, and two responses (automatic attack disruption; analysts with Defender Experts MDR). A dashed loop carries containment back to the signal sources. It makes no new claims; every label restates the body text.
- **Icons:** three official icons from the Microsoft Azure architecture icon set (V24, July 2026, https://learn.microsoft.com/en-us/azure/architecture/icons/), copied unmodified to `site/assets/icons/azure/`: `sentinel.svg` (Azure Sentinel), `entra-id-protection.svg` (Entra ID Protection, on the Identity chip) and `ai-foundry.svg` (AI Foundry, on the AI apps & agents chip). They are loaded with `<image>`, so the files stay byte-identical to Microsoft's. The caption credits "Microsoft Azure architecture icons".
- **Terms:** Microsoft allows these icons "in architectural diagrams, training materials, or documentation", unmodified (no cropping, flipping, rotating or distortion). Defender XDR, Security Copilot, Purview and the Defender workloads have no official architecture icon (not in the Azure V24 set; the archived Microsoft 365 set has no security icons), so those boxes stay text-only. The Entra icon set was deliberately not used because its terms also forbid use in marketing communications, and the post ends with a consulting call to action.
- **QA:** `blog-visual-audit.js` passes locally, including T21 (all assets load). The only WARN is T06 mobile paragraph length, which was already there with the same count (20) before this change. Checked in dark mode, light mode and at 390px phone width.
- **Follow-up, same day: icons on the layered reference architecture (dgB).** Official Azure V24 icons were added above the titles of 8 of its 12 boxes: Front Door (`front-door.svg`), API Management (`api-management.svg`), Entra ID + Agent ID (`entra-id-protection.svg`), Microsoft Foundry (`ai-foundry.svg`), Azure AI Search (`ai-search.svg`, Microsoft's Cognitive Search icon), Data stores (`private-endpoints.svg`), Defender for Cloud (`defender-for-cloud.svg`) and Microsoft Sentinel (`sentinel.svg`). AI threat protection, Purview, Defender XDR and Security Copilot stay text-only. AI threat protection is a Defender for Cloud plan, so it gets no icon rather than a repeat of the Defender for Cloud one; the other three have no official icon. Boxes grew from 92 to 104 units to fit the icons (viewBox 720 → 768). All text is unchanged, and the caption now credits the icons. The local audit result is the same as before.

## Post B figure: offers mapped to the 180-day roadmap (1 October 2026)

- **What:** the first inline SVG in Post B (`dgP`), placed in "From Pitch to Delivery" between the intro paragraph and the phase/offer table, which stays for the detail. It shows the customer roadmap phases (0–30 identity and onboarding, 30–90 one portal and attack disruption, 90–180 AI protection at scale), the fixed-fee offer under each phase, and the recurring managed SOC (MXDR or co-managed, monthly posture review) starting at day 90 and running past day 180. Not to scale, and the caption says so.
- **Content rule:** every label restates the post's existing text. It deliberately leaves out the partner details still awaiting the owner's sign-off ($2K per briefing, CSP incentive rates, Business Case Builder detail, "5–25 customers").
- **Icons:** Azure V24 icons on the three offers (Entra ID Protection, Sentinel, Foundry), reusing the files already in `site/assets/icons/azure/`. The managed SOC has no icon because Defender XDR has no official one.
- **QA:** checked text fit by measuring each label against its box (one overflow fixed by shortening it to "→ recurring governance"), and rendered in dark, light and 390px phone. The local audit passes; T06 mobile WARN was there before.

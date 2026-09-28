# Blog Readability — PDCA Plan & To-Do Tracker

**Owner:** Upendra Kumar  **Created:** 2026-09-28  **Status:** Cycle 1 not started

**Goal:** make blog posts easy to read on desktop and phone, then make the fixes permanent so new posts don't reintroduce the problems.

| Cycle | Scope | Items | Done |
|---|---|---|---|
| 1 | The unified SecOps post (`site/blog/2026-09-28-unified-security-operations-ai-era.html`) | 10 | 0 / 10 |
| 2 | Shared blog template: `css/premium.css` and all 49 posts | 10 | 0 / 10 |
| Act | Make it stick: BlogMaker template, publishing gate, review | 4 | 0 / 4 |

---

## How testing and validation work

Every to-do item is tied to one or more automated checks (T01–T21). Each check runs at **two screen sizes**:

- **Desktop:** 1440 × 900
- **Mobile:** 390 × 844, an iPhone-sized touch screen at 2× pixel density

The validator is `tools/qa/blog-visual-audit.js`. For each check it records PASS / FAIL / WARN / N/A with the measured value, saves a screenshot of every failing element for each screen size, and writes a report.

### Commands (run from the repo root)

```powershell
# 1. Before deploy: test your local edits
node tools/qa/blog-visual-audit.js 2026-09-28-unified-security-operations-ai-era

# Only the checks for the item you're working on
node tools/qa/blog-visual-audit.js 2026-09-28-unified-security-operations-ai-era --only=T03,T13

# Add full-page screenshots (one per screen height) for a manual scroll-through
node tools/qa/blog-visual-audit.js 2026-09-28-unified-security-operations-ai-era --slices

# 2. After deploy: test the live site (cache-busted, so Cloudflare can't serve an old copy)
node tools/qa/blog-visual-audit.js 2026-09-28-unified-security-operations-ai-era --live

# 3. Cycle 2: every post at once (summary only)
node tools/qa/blog-visual-audit.js --all
node tools/qa/blog-visual-audit.js --all --live
```

- **Reports:** `tools/qa/reports/<post>/<timestamp>-<local|live>/report.md`. Screenshots are in `desktop/` and `mobile/` next to the report. The folder is git-ignored.
- **Exit code:** 1 if any check fails, so the audit can gate a deploy.
- If `node` isn't on PATH, use `& "$env:ProgramFiles\nodejs\node.exe"`.

### Definition of done (every item)

An item is done only when all four boxes are ticked:

1. **Implemented:** the change is made in the file(s) listed.
2. **Desktop validated:** the linked checks PASS at 1440 in a local run, and the desktop screenshot or slice looks right.
3. **Mobile validated:** the linked checks PASS at 390 in a local run, and the mobile screenshot or slice looks right.
4. **Live validated:** the same checks PASS on the `--live` run after deploy, on both sizes.

**Manual visual check:** the numbers catch measurable problems, not taste. For every item, open the `--slices` screenshots for both sizes and confirm the change looks intended: nothing overlapping, clipped or oddly spaced.

---

## Check reference and baseline

Baseline: live site, 2026-09-28 10:46 (report `20260928-104646-live`). Targets are what "PASS" means.

| ID | Check | Target | Desktop baseline | Mobile baseline |
|---|---|---|---|---|
| T01 | No sideways page scroll | 0px | ✅ 0px | ❌ 60px wider (hero section) |
| T02 | Glossary underlines: first use only, none in components | ≤1 per term, 0 in components | ❌ 42 total, "XDR" ×17, 24 in components | ❌ same |
| T03 | Executive summary cards readable | Desktop ≤5 lines or ≥480px wide; mobile ≤10 lines | ❌ 22 lines, 163px wide | ❌ 13 lines |
| T04 | Tables show all columns | 0 tables needing sideways scroll | ✅ 0/3 | ❌ 3/3 |
| T05 | Timeline steps short | Desktop ≤2 lines, mobile ≤3 | ❌ 6 lines | ✅ |
| T06 | Paragraph length | 0 paragraphs over 4 lines (desktop) | ❌ 10 (longest 7) | ⚠️ info only |
| T07 | Type scale | ≤3 body text sizes | ❌ 4 (18.4/15.2/14.4/13.6px) | ❌ 4 |
| T08 | Body line height | 1.55–1.75 | ❌ 1.90 | ❌ 1.90 |
| T09 | Small / low-contrast text | ≥13px (≥12px for uppercase labels), contrast ≥4.5 | ❌ 26 elements | ❌ 26 elements |
| T10 | Share button icons render | 0 missing | ❌ X/Twitter missing | ❌ X/Twitter missing |
| T11 | Contents sidebar tracks position | All sections | ❌ 13/14 (first section never highlights) | ➖ sidebar hidden |
| T12 | Checkboxes match theme | accent colour set | ❌ browser default | ❌ browser default |
| T13 | No watermark icons behind text | 0 | ❌ 3 | ❌ 3 |
| T14 | Footer centred | ≤4px off | ❌ 154px off | ✅ |
| T15 | Opening paragraph length | Desktop ≤5 lines, mobile ≤6 | ❌ 6 | ❌ 13 |
| T16 | Stat tiles compact | Desktop labels ≤3 lines; mobile 4-tile block 2 per row | ❌ 4-line label | ❌ 1 per row |
| T17 | Gap between hero tags and article | Desktop ≤120px, mobile ≤96px | ❌ 157px | ❌ 157px |
| T18 | No orphaned word in headings | 0 | ❌ "…Workloads on Azure" | ❌ 2 ("24/7 Without Hiring 24/7") |
| T19 | Author note uses card width (mobile) | ≥80% | ✅ info only | ❌ 67% |
| T20 | Particles hidden behind article text | Article background opacity ≥0.85, or particles off | ❌ transparent | ❌ transparent |
| T21 | No script errors or broken assets | 0 / 0 | ✅ | ✅ |

---

## PLAN

### Principles

- **Prove on one post, then roll out.** Cycle 1 changes only the new post; Cycle 2 touches shared CSS and all posts.
- **Fix at the right layer.** Each post carries its own copy of its styles and scripts, so a fix goes into the shared CSS where possible (one change, every page) or into a patch script with a dry run where it can't.
- **Measure before and after** with the same tool, at the same two sizes, locally and live.

### Risks

| Risk | Mitigation |
|---|---|
| Patch script breaks an older post | Exact-match replacements only; dry run lists the changes; review 3 sample posts; one commit per item so `git revert` is clean |
| Shared CSS change alters older posts' look | Run `--all` before and after; compare `--slices` on 5 sample posts |
| Wrong icon-library file hash, so all icons disappear | Copy the hash from cdnjs, test one page with T10 before rolling out |
| Cloudflare serves the old page | Always validate live with `--live` (it adds `?v=<timestamp>`); edges refresh in about 25–30 minutes |
| Azure deploy targets the wrong subscription | `az account set --subscription 87cf2b93-5e52-4533-9e6b-7182cd7dbde6` before `tools/deploy/deploy-azure.ps1` |

---

## DO — Cycle 1: the unified SecOps post

File for every item: `site/blog/2026-09-28-unified-security-operations-ai-era.html`, in its body HTML or its own `<style>` block.

### C1-01 · Executive summary cards

**Checks:** T03, T13  **Baseline:** 22-line cards, 163px text width, 3 watermark icons

**Change:**
- Stack the three cards as full-width rows: icon on the left, heading and text on the right, one card per row.
- Cut each card to about 3 lines, with the key number in bold.
- Remove the `opacity: 0.03` watermark icons.

**Look for:**
- Desktop: three short horizontal bands, each readable in one glance.
- Mobile: the icon sits above the text, and no card is taller than about 10 lines.

- [ ] Implemented
- [ ] Desktop validated: T03 ✅, T13 ✅, screenshot checked
- [ ] Mobile validated: T03 ✅, T13 ✅, screenshot checked
- [ ] Live validated

### C1-02 · Tables readable on phone

**Checks:** T04  **Baseline:** 3 of 3 tables hide columns on mobile

**Change:**
- Add a `.stack-table` style. Below 768px, hide the header row and show each row as a card with labelled fields ("Threat" / "What it looks like" / "Controls").
- Apply it to all three tables: threats, suite pricing and solution plays.

**Look for:**
- Desktop: the tables are unchanged.
- Mobile: every field is visible without scrolling sideways, and the labels are readable.

- [ ] Implemented
- [ ] Desktop validated: T04 ✅
- [ ] Mobile validated: T04 ✅, screenshot checked
- [ ] Live validated

### C1-03 · Attack-disruption timelines

**Checks:** T05  **Baseline:** 6-line steps on desktop

**Change:** use the vertical timeline at every width for the 7-step incident, or cut each step to 4 words or fewer. Keep the 4-step incident horizontal if it passes.

**Look for:**
- Desktop: every step reads in 1–2 lines, and the time labels line up.
- Mobile: the vertical line and dots stay aligned.

- [ ] Implemented
- [ ] Desktop validated: T05 ✅
- [ ] Mobile validated: T05 ✅
- [ ] Live validated

### C1-04 · Break up the text walls

**Checks:** T06, T08  **Baseline:** 10 paragraphs over 4 lines; line height 1.90

**Change:**
- Split every paragraph over 4 lines.
- Turn "The two loops that do most of the work" into 2 side-by-side cards.
- Turn "The win formula, stage by stage" into numbered step cards.
- Set body `line-height: 1.7` in this post's style block. Cycle 2 fixes the shared rule behind it.

**Look for:**
- Desktop: no block of text taller than about 4 lines without a break.
- Mobile: the text is still comfortable to read, not cramped.

- [ ] Implemented
- [ ] Desktop validated: T06 ✅, T08 ✅
- [ ] Mobile validated: T08 ✅
- [ ] Live validated

### C1-05 · Consistent type scale and readable small text

**Checks:** T07, T09  **Baseline:** 4 body sizes; 26 small or low-contrast elements

**Change:**
- Body text 1.1rem; compact text in cards, timelines and tables 0.95rem; captions 0.85rem. That is three sizes in total.
- Source notes and stat sources: at least 13px, colour `#94a3b8` or lighter.

**Look for:**
- Both sizes: cards and body no longer feel like different documents, and grey footnotes are easy to read.

- [ ] Implemented
- [ ] Desktop validated: T07 ✅, T09 ✅
- [ ] Mobile validated: T07 ✅, T09 ✅
- [ ] Live validated

### C1-06 · Stat tiles

**Checks:** T16  **Baseline:** 4-line label on desktop; 1 tile per row on mobile

**Change:**
- Shorten "additional IT & security headcount avoided" to "headcount avoided", and every label to 2 lines or fewer.
- On mobile, show `.stat-quad` two per row (`grid-template-columns: 1fr 1fr` under 768px).

**Look for:**
- Desktop: all four tiles are the same height.
- Mobile: the 2×2 grid fits in about half a screen.

- [ ] Implemented
- [ ] Desktop validated: T16 ✅
- [ ] Mobile validated: T16 ✅, screenshot checked
- [ ] Live validated

### C1-07 · Opening paragraph

**Checks:** T15  **Baseline:** 6 lines on desktop, 13 on mobile

**Change:**
- Cut to 2 sentences, e.g. "Attackers need 72 minutes from a phishing click to your data. Stolen-credential breaches take 292 days to contain — and AI agents are widening the gap."
- Font size 1.2rem under 768px.

**Look for:**
- Both sizes: it reads as a hook, not a wall.

- [ ] Implemented
- [ ] Desktop validated: T15 ✅
- [ ] Mobile validated: T15 ✅
- [ ] Live validated

### C1-08 · Author note on phone

**Checks:** T19  **Baseline:** text uses 67% of the card on mobile

**Change:** add class `author-note`. Under 768px, put the icon above the text (`flex-direction: column; align-items: flex-start`).

**Look for:**
- Mobile: the text runs the full card width.

- [ ] Implemented
- [ ] Desktop validated: no visual change
- [ ] Mobile validated: T19 ✅
- [ ] Live validated

### C1-09 · Hero spacing and heading orphans

**Checks:** T17, T18  **Baseline:** 157px gap; "…on Azure" and "24/7 Without Hiring 24/7" wrap badly

**Change:**
- Reduce the gap between the hero and the article: article top padding about 2rem, hero bottom padding about 2rem.
- Rename the heading to "Reference Architecture".
- Add `text-wrap: balance` to `h2`, `h3` in the post style. Rename "24/7 Without Hiring 24/7" if it still orphans.

**Look for:**
- Both sizes: the opening paragraph follows the tags without a void, and no heading ends in one lonely word.

- [ ] Implemented
- [ ] Desktop validated: T17 ✅, T18 ✅
- [ ] Mobile validated: T17 ✅, T18 ✅
- [ ] Live validated

### C1-10 · Sideways scroll on phone

**Checks:** T01  **Baseline:** 60px overflow on mobile, which the validator traced to the hero section

**Change:**
- Open `mobile/T01-*.png` from the latest report to find the overflowing element.
- Constrain it (`max-width: 100%`, `overflow-wrap: anywhere`, or fix the offending width).
- If the cause turns out to be shared, move this item to C2-07.

**Look for:**
- Mobile: the page doesn't shift sideways when you swipe.

- [ ] Implemented
- [ ] Desktop validated: T01 ✅
- [ ] Mobile validated: T01 ✅
- [ ] Live validated

### Cycle 1 release

- [ ] Local run: all Cycle 1 checks (T01, T03–T09, T13, T15–T19) PASS on both sizes
- [ ] `--slices` run reviewed, desktop and mobile, top to bottom
- [ ] Commit "Readability pass: unified SecOps post" (post file only), then `git push origin main`
- [ ] `az account set --subscription 87cf2b93-…`, then `tools/deploy/deploy-azure.ps1`
- [ ] `--live` run: the same checks PASS on both sizes; result logged in the test log below

---

## DO — Cycle 2: shared template (all posts)

### Cycle 2 baseline: posts failing each check

Local run `20260928-104724-local`, 49 posts. T21 was re-run after excluding the Cloudflare analytics beacon, which can't send from a page loaded off disk.

| Check | Posts failing | Check | Posts failing |
|---|---|---|---|
| T01 sideways scroll | 25 | T12 checkboxes | 5 |
| T02 glossary | 12 | T13 watermarks | 9 |
| T03 summary cards | 10 | T14 footer | 40 |
| T04 tables | 2 | T15 opening paragraph | 18 |
| T05 timelines | 1 | T16 stat tiles | 1 |
| T06 paragraph length | 24 | T17 hero gap | 23 |
| T07 type scale | 31 | T18 heading orphans | 35 |
| T08 line height | 46 | T19 author note | 4 |
| T09 small text | 39 | T20 particles | 44 |
| T10 share icon | 42 | T21 broken assets | 19 |
| T11 contents sidebar | 13 | | |

Cycle 2 targets the **template** checks: T01, T02, T08, T10–T14, T20, T21. The content checks (T03–T07, T09, T15–T19) depend on each post's writing and layout; fix those per post in Cycle 3.

Patch script for per-post edits: `tools/scripts/patch-blog-template.js`, to be written. It must:
- run with `--dry-run` by default;
- use exact-match replacements only;
- report "changed / already fixed / pattern not found" for each post.

### C2-01 · Twitter/X share icon

**Checks:** T10  **Scope:** posts loading Font Awesome 6.4.0 (46 posts; 41 use `fa-x-twitter`)

**Change:** in every post, point the Font Awesome link to 6.5.x and replace its `integrity` hash with the one cdnjs publishes for that file.

- [ ] Implemented
- [ ] Desktop validated
- [ ] Mobile validated
- [ ] Live validated

### C2-02 · Glossary underlines

**Checks:** T02  **Scope:** 11 posts with `glossaryTerms`

**Change:** in the glossary script, underline only the first match per term, and skip `.glass-card, .mini-card, .incident, table, .stat-tile, strong, .arch-stack, .checklist-item`.

- [ ] Implemented
- [ ] Desktop validated
- [ ] Mobile validated
- [ ] Live validated

### C2-03 · Contents sidebar highlighting

**Checks:** T11 (desktop only)  **Scope:** 13 posts with `.toc-container`

**Change:** replace the IntersectionObserver with a scroll handler that marks the last heading above `top + 150px` as active, and the last link at page bottom.

- [ ] Implemented
- [ ] Desktop validated
- [ ] Mobile validated: N/A, the sidebar is hidden on phones
- [ ] Live validated

### C2-04 · Particles behind text

**Checks:** T20  **Scope:** `css/premium.css` covers 45 posts at once

**Change:** give `.blog-post-content` a near-opaque background (e.g. `rgba(10,10,15,0.92)`, rounded) or lower the particle opacity behind content.

- [ ] Implemented
- [ ] Desktop validated
- [ ] Mobile validated
- [ ] Live validated

### C2-05 · Themed checkboxes

**Checks:** T12  **Scope:** `css/premium.css`

**Change:** add `.checklist-container input[type="checkbox"] { accent-color: #38bdf8; width: 1.1rem; height: 1.1rem; }`.

- [ ] Implemented
- [ ] Desktop validated
- [ ] Mobile validated
- [ ] Live validated

### C2-06 · Footer alignment

**Checks:** T14  **Scope:** `css/premium.css`

**Change:** centre `footer .container > p` (`text-align: center`) and the social links.

- [ ] Implemented
- [ ] Desktop validated
- [ ] Mobile validated
- [ ] Live validated

### C2-07 · Sideways scroll on phones, all posts

**Checks:** T01  **Scope:** `css/premium.css`, plus the posts named in the `--all` report

**Change:** fix the shared cause found in C1-10. Then clear any post-specific overflow the `--all` report lists.

- [ ] Implemented
- [ ] Desktop validated
- [ ] Mobile validated
- [ ] Live validated

### C2-08 · Watermark icons

**Checks:** T13  **Scope:** 8 posts with `opacity: 0.03` icons

**Change:** the patch script removes the watermark `<div>`s from the executive-summary cards.

- [ ] Implemented
- [ ] Desktop validated
- [ ] Mobile validated
- [ ] Live validated

### C2-09 · Body line height and cache refresh

**Checks:** T08, T21  **Scope:** `css/premium.css` / `css/style.css`, and all posts

**Change:**
- Find the shared rule that forces 1.9 line height and set it to 1.7.
- Bump the stylesheet version in every post (`?v=49` → `?v=50`) so browsers fetch the new CSS.
- Confirm T21 (no errors, no broken assets) on all posts.

- [ ] Implemented
- [ ] Desktop validated
- [ ] Mobile validated
- [ ] Live validated

### C2-10 · Broken embeds and images

**Checks:** T21  **Scope:** 19 posts. These fail live too, so they are real.

**Examples found:**
- A LinkedIn embed that returns 404 (`urn:li:share:7411068804652257280`, in `2025-12-27-model-context-protocol`).
- `assets/images/poster_default.webp` missing locally (`2026-01-17-document-intelligence-copilot-azure`).
- YouTube `hqdefault.webp` thumbnails that return 404: use `hqdefault.jpg` instead.

**Change:** run `--all --only=T21` and fix or remove each failing URL. The report names the first failing request per post; re-run until clean.

- [ ] Implemented
- [ ] Desktop validated
- [ ] Mobile validated
- [ ] Live validated

### Cycle 2 release

- [ ] Patch script dry run reviewed; diffs of 3 sample posts read (one each from 2025, early 2026 and Sept 2026)
- [ ] `--all` local run: the template checks (T01, T02, T08, T10–T14, T20, T21) have fewer failing posts than the baseline, and none got worse
- [ ] `--slices` reviewed on 5 sample posts, desktop and mobile
- [ ] One commit per item, then push, then Azure deploy
- [ ] `--all --live` run logged

---

## CHECK

| Gate | How | Pass condition |
|---|---|---|
| Per item | `--only=<checks>` local, both sizes | Linked checks PASS; screenshots look right |
| Per cycle, before deploy | Full local run (`--all` for Cycle 2) + `--slices` review | All in-scope checks PASS; no check that passed before now fails |
| Per cycle, after deploy | `--live` (`--all --live` for Cycle 2) | Same result as local |
| Speed | Compare page load before and after in browser dev tools, or with the Playwright timing | No slower |

**If a check fails:** go back to DO for that item only. If it can't be met, write it in the Exceptions table with the reason.

### Exceptions

| Item / check | Reason accepted | Date |
|---|---|---|
| — | — | — |

---

## ACT — make it stick

### A-01 · Update the BlogMaker template

**File:** `tools/content/master prompts/blogmaker.md`

**Change:** add the new standards: stacked executive cards with no watermarks, `.stack-table` for tables, first-use-only glossary, the three-size type scale, line height 1.7, Font Awesome 6.5.x, a 2-sentence lead, and `text-wrap: balance` on headings.

- [ ] Done

### A-02 · Publishing gate

**Change:** add to BlogMaker's final steps: "Run `node tools/qa/blog-visual-audit.js <post>`; publish only if it exits 0. After deploy, run it again with `--live`."

- [ ] Done

### A-03 · Record the rules

**Change:** update the portfolio memory notes with the audit tool, the patch script and the new template rules.

- [ ] Done

### A-04 · 30-day review (due 2026-10-28)

**Change:** compare App Insights time on page and scroll depth for this post against the VMware post. Plan Cycle 3 with the older 2025 posts in batches of about 10.

- [ ] Done

---

## Test run log

Add a row after every validation run.

| Date | Scope | Source | Report folder | Desktop fails | Mobile fails | Notes |
|---|---|---|---|---|---|---|
| 2026-09-28 | SecOps post | live | `20260928-104646-live` | 17 | 16 | Baseline before any changes |
| 2026-09-28 | All 49 posts | local | `_all/20260928-104724-local` | see Cycle 2 baseline | see Cycle 2 baseline | Baseline; T21 re-run with the Cloudflare beacon excluded, 19 posts |

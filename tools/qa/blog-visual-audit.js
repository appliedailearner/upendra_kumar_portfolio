#!/usr/bin/env node
/*
 * Blog visual audit — validates readability fixes on desktop (1440x900) and mobile (390x844).
 *
 * Every check has an ID (T01…T21) that the tracker in
 * project-docs/BLOG_READABILITY_PDCA_PLAN.md references, so each to-do item has an
 * automated pass/fail on both screen sizes plus screenshots of anything that fails.
 *
 * Usage (from repo root):
 *   node tools/qa/blog-visual-audit.js <post>                 local file in site/blog (before deploy)
 *   node tools/qa/blog-visual-audit.js <post> --live          live site, cache-busted (after deploy)
 *   node tools/qa/blog-visual-audit.js https://…/post.html    any URL
 *   node tools/qa/blog-visual-audit.js --all [--live]         every post in site/blog (summary only)
 *
 * <post> is a file name with or without .html, e.g. 2026-09-28-unified-security-operations-ai-era
 *
 * Options:
 *   --viewport=desktop|mobile|both   default both
 *   --only=T02,T04                   run a subset of checks
 *   --slices                         also save full-page screenshots, one per screen height
 *   --out=<dir>                      report folder (default tools/qa/reports/<post>/<timestamp>-<local|live>)
 *
 * Exit code 1 if any check FAILs, so it can gate a deploy.
 */
const fs = require('fs');
const path = require('path');
const { pathToFileURL } = require('url');
const { chromium } = require('playwright-chromium');

const REPO = path.resolve(__dirname, '..', '..');
const BLOG_DIR = path.join(REPO, 'site', 'blog');
const LIVE_BASE = 'https://portfolio.upendrakumar.com';
const VIEWPORTS = {
    desktop: { viewport: { width: 1440, height: 900 } },
    mobile: { viewport: { width: 390, height: 844 }, isMobile: true, hasTouch: true, deviceScaleFactor: 2 },
};
const IGNORED_REQUEST_HOSTS = ['dc.services.visualstudio.com', 'js.monitor.azure.com', 'liana.ice.azure.microsoft.com', 'google-analytics', 'googletagmanager', 'cloudflareinsights.com'];

// ---------- argument parsing ----------
const args = process.argv.slice(2);
const flag = (name) => args.includes(`--${name}`);
const opt = (name, def) => {
    const a = args.find((x) => x.startsWith(`--${name}=`));
    return a ? a.split('=').slice(1).join('=') : def;
};
const positional = args.filter((a) => !a.startsWith('--'));
const LIVE = flag('live');
const VIEWPORT_SEL = opt('viewport', 'both');
const ONLY = opt('only', '') ? opt('only').split(',').map((s) => s.trim().toUpperCase()) : null;
const stamp = new Date().toISOString().replace(/[-:]/g, '').replace('T', '-').slice(0, 15);

function resolveTarget(t) {
    if (/^https?:\/\//.test(t)) return { name: path.basename(new URL(t).pathname, '.html'), url: t, mode: 'url' };
    const file = t.endsWith('.html') ? path.basename(t) : `${path.basename(t)}.html`;
    const name = file.replace(/\.html$/, '');
    if (LIVE) return { name, url: `${LIVE_BASE}/blog/${file}?v=${Date.now()}`, mode: 'live' };
    const local = path.join(BLOG_DIR, file);
    if (!fs.existsSync(local)) throw new Error(`Not found: ${local}`);
    return { name, url: pathToFileURL(local).href, mode: 'local' };
}

// ---------- in-page checks (run inside the browser) ----------
function pageChecks(vp) {
    const out = [];
    const content = document.querySelector('.blog-post-content') || document.body;
    const cw = document.documentElement.clientWidth;
    let tagN = 0;
    const tag = (el, id) => {
        const key = `${id}-${tagN++}`;
        el.setAttribute('data-audit-id', key);
        return key;
    };
    const visible = (el) => {
        const r = el.getBoundingClientRect();
        const s = getComputedStyle(el);
        return r.width > 0 && r.height > 0 && s.visibility !== 'hidden' && s.display !== 'none';
    };
    // Rendered text lines of an element: rects of its text nodes (icons ignored), merged when
    // they overlap vertically, so an inline icon or a taller bold span doesn't count as a line.
    const textLines = (el) => {
        const walker = document.createTreeWalker(el, NodeFilter.SHOW_TEXT);
        const rects = [];
        for (let n = walker.nextNode(); n; n = walker.nextNode()) {
            if (!n.textContent.trim() || (n.parentElement && n.parentElement.closest('i, svg'))) continue;
            const range = document.createRange();
            range.selectNodeContents(n);
            for (const r of range.getClientRects()) if (r.width > 1 && r.height > 1) rects.push({ top: r.top, bottom: r.bottom, left: r.left, right: r.right });
        }
        rects.sort((a, b) => a.top - b.top);
        const merged = [];
        for (const r of rects) {
            const last = merged[merged.length - 1];
            const overlap = last ? Math.min(last.bottom, r.bottom) - Math.max(last.top, r.top) : 0;
            if (last && overlap > 0.5 * Math.min(last.bottom - last.top, r.bottom - r.top)) {
                last.left = Math.min(last.left, r.left); last.right = Math.max(last.right, r.right);
                last.top = Math.min(last.top, r.top); last.bottom = Math.max(last.bottom, r.bottom);
            } else merged.push({ ...r });
        }
        return merged;
    };
    const lines = (el) => textLines(el).length;
    const lineRects = (el) => textLines(el).map((l) => l.right - l.left);
    const rgba = (s) => {
        const m = s.match(/rgba?\(([^)]+)\)/);
        if (!m) return [0, 0, 0, 0];
        const p = m[1].split(/[ ,/]+/).filter(Boolean).map(Number);
        return [p[0], p[1], p[2], p.length > 3 ? p[3] : 1];
    };
    // Returns null when a gradient/image background sits behind the text: contrast can't be computed reliably.
    const effectiveBg = (el) => {
        const stack = [];
        for (let n = el; n && n.nodeType === 1; n = n.parentElement) {
            const cs = getComputedStyle(n);
            if (cs.backgroundImage && cs.backgroundImage !== 'none' && stack.every((c) => c[3] < 1)) return null;
            const c = rgba(cs.backgroundColor);
            if (c[3] > 0) stack.push(c);
            if (c[3] >= 1) break;
        }
        let bg = rgba(getComputedStyle(document.body).backgroundColor);
        if (bg[3] < 1) bg = [10, 10, 15, 1];
        for (const c of stack.reverse()) bg = [0, 1, 2].map((i) => c[i] * c[3] + bg[i] * (1 - c[3])).concat(1);
        return bg;
    };
    const lum = ([r, g, b]) => {
        const f = (v) => { v /= 255; return v <= 0.03928 ? v / 12.92 : Math.pow((v + 0.055) / 1.055, 2.4); };
        return 0.2126 * f(r) + 0.7152 * f(g) + 0.0722 * f(b);
    };
    const contrast = (a, b) => { const [x, y] = [lum(a), lum(b)].sort((p, q) => q - p); return (x + 0.05) / (y + 0.05); };
    const add = (id, title, status, value, target, offenders = []) => out.push({ id, title, status, value: String(value), target, offenders });
    const NA = (id, title, why) => add(id, title, 'N/A', why, '-');

    // T01 — no horizontal page overflow
    {
        const over = document.documentElement.scrollWidth - cw;
        // Fixed-position layers (navbar, particle canvas) stretch to the widened page, so they're symptoms, not causes.
        // Hidden pseudo-element tooltips can also cause overflow but aren't elements; if no offender is listed, check ::after rules.
        const offenders = [...document.querySelectorAll('body *')]
            .filter((e) => visible(e) && e.getBoundingClientRect().right > cw + 1 && !e.closest('.table-scroll'))
            .filter((e) => !e.closest('.navbar, #particles-canvas') && getComputedStyle(e).position !== 'fixed')
            .filter((e) => !e.parentElement || !(e.parentElement.getBoundingClientRect().right > cw + 1))
            .slice(0, 3).map((e) => tag(e, 'T01'));
        add('T01', 'No sideways page scroll', over <= 0 ? 'PASS' : 'FAIL', `${over}px wider than screen`, '0px', offenders);
    }

    // T02 — glossary underlines: first occurrence only, never inside components
    {
        const terms = [...document.querySelectorAll('.eli5-term')];
        const per = {};
        terms.forEach((t) => { per[t.textContent] = (per[t.textContent] || 0) + 1; });
        const maxPer = Math.max(0, ...Object.values(per));
        const inComp = terms.filter((t) => t.closest('.glass-card, .mini-card, .incident, table, .stat-tile, strong, .arch-stack, .checklist-item'));
        if (!terms.length) NA('T02', 'Glossary underlines', 'no glossary terms');
        else add('T02', 'Glossary underlines (first use only, none in components)', maxPer <= 1 && !inComp.length ? 'PASS' : 'FAIL',
            `${terms.length} total, max ${maxPer} per term, ${inComp.length} inside components`, '≤1 per term, 0 in components',
            inComp.slice(0, 2).map((e) => tag(e.closest('.glass-card, .mini-card, .incident, table, .stat-tile, p, li') || e, 'T02')));
    }

    // T03 — executive summary cards readable
    {
        const ps = [...document.querySelectorAll('.executive-grid .glass-card p, .exec-rows .exec-row p')];
        if (!ps.length) NA('T03', 'Executive summary cards', 'no executive summary');
        else {
            const maxL = Math.max(...ps.map(lines));
            const minW = Math.min(...ps.map((p) => p.getBoundingClientRect().width));
            const limit = vp === 'desktop' ? 5 : 10;
            const ok = maxL <= limit || (vp === 'desktop' && minW >= 480);
            add('T03', 'Executive summary cards', ok ? 'PASS' : 'FAIL', `max ${maxL} lines, narrowest text ${Math.round(minW)}px`,
                vp === 'desktop' ? '≤5 lines or ≥480px wide' : '≤10 lines', ok ? [] : [tag(document.querySelector('.executive-grid, .exec-rows'), 'T03')]);
        }
    }

    // T04 — tables show every column without hidden sideways scroll
    {
        const wraps = [...document.querySelectorAll('.table-scroll')];
        if (!wraps.length) NA('T04', 'Tables fit the screen', 'no tables');
        else {
            const bad = wraps.filter((w) => w.scrollWidth > w.clientWidth + 1);
            add('T04', 'Tables fit the screen (all columns visible)', bad.length ? 'FAIL' : 'PASS',
                `${bad.length}/${wraps.length} tables need sideways scroll`, '0', bad.slice(0, 2).map((e) => tag(e, 'T04')));
        }
    }

    // T05 — timeline steps are short
    {
        const steps = [...document.querySelectorAll('.incident-steps li')];
        if (!steps.length) NA('T05', 'Timeline step length', 'no timeline');
        else {
            const maxL = Math.max(...steps.map((li) => lines(li) - (li.querySelector('.t') ? 1 : 0)));
            const limit = vp === 'desktop' ? 2 : 3;
            add('T05', 'Timeline step length', maxL <= limit ? 'PASS' : 'FAIL', `longest step ${maxL} lines`, `≤${limit} lines`,
                maxL <= limit ? [] : [tag(document.querySelector('.incident'), 'T05')]);
        }
    }

    // T06 — no walls of text (desktop measure)
    {
        const ps = [...content.querySelectorAll(':scope > p')].filter((p) => !p.classList.contains('lead') && visible(p));
        const long = ps.filter((p) => lines(p) > 4);
        const maxL = Math.max(0, ...ps.map(lines));
        add('T06', 'Paragraph length', long.length ? (vp === 'desktop' ? 'FAIL' : 'WARN') : 'PASS',
            `${long.length} paragraphs over 4 lines (longest ${maxL})`, vp === 'desktop' ? '0 over 4 lines' : 'info only on mobile',
            long.slice(0, 3).map((e) => tag(e, 'T06')));
    }

    // T07 — consistent type scale in body text
    {
        const isLabel = (e) => { const cs = getComputedStyle(e); return cs.textTransform === 'uppercase' && parseFloat(cs.letterSpacing) > 0; }; // eyebrow labels aren't body text
        const els = [...content.querySelectorAll('p, li, td')].filter((e) => visible(e) && !isLabel(e) && !e.closest('.lead, .toc-container, .social-share-container, .stat-tile, .blog-post-meta'));
        const sizes = [...new Set(els.map((e) => getComputedStyle(e).fontSize))].sort((a, b) => parseFloat(b) - parseFloat(a));
        add('T07', 'Type scale (distinct body sizes)', sizes.length <= 3 ? 'PASS' : 'FAIL', `${sizes.length}: ${sizes.join(', ')}`, '≤3 (body, compact, caption)');
    }

    // T08 — body line height
    {
        const p = [...content.querySelectorAll(':scope > p')].find((x) => !x.classList.contains('lead') && visible(x));
        if (!p) NA('T08', 'Body line height', 'no body paragraph');
        else {
            const s = getComputedStyle(p);
            const ratio = parseFloat(s.lineHeight) / parseFloat(s.fontSize);
            add('T08', 'Body line height', ratio >= 1.55 && ratio <= 1.75 ? 'PASS' : 'FAIL', `${ratio.toFixed(2)} (${s.fontSize}/${s.lineHeight})`, '1.55–1.75');
        }
    }

    // T09 — small or low-contrast text
    {
        const bad = [];
        for (const el of content.querySelectorAll('*')) {
            if (!visible(el) || el.closest('.toc-container, svg')) continue; // SVG text scales with the drawing
            const hasText = [...el.childNodes].some((n) => n.nodeType === 3 && n.textContent.trim().length > 1);
            if (!hasText) continue;
            const s = getComputedStyle(el);
            if (s.webkitTextFillColor && s.webkitTextFillColor.includes('rgba(0, 0, 0, 0)')) continue; // gradient text
            const fs = parseFloat(s.fontSize);
            const bg = effectiveBg(el);
            const c = bg ? contrast(rgba(s.color), bg) : 21;
            // Letter-spaced uppercase eyebrow labels read fine down to 12px.
            const minSize = s.textTransform === 'uppercase' && parseFloat(s.letterSpacing) > 0 ? 12 : 13;
            if (fs < minSize || c < 4.5) bad.push({ el, why: `${fs}px, contrast ${c.toFixed(1)}` });
        }
        add('T09', 'Small / low-contrast text', bad.length ? 'FAIL' : 'PASS',
            bad.length ? `${bad.length} elements, e.g. "${bad[0].el.textContent.trim().slice(0, 40)}" (${bad[0].why})` : 'none', '≥13px and contrast ≥4.5',
            bad.slice(0, 3).map((b) => tag(b.el, 'T09')));
    }

    // T10 — share buttons all have icons
    {
        const icons = [...document.querySelectorAll('.share-btn i')];
        if (!icons.length) NA('T10', 'Share button icons', 'no share buttons');
        else {
            const bad = icons.filter((i) => { const c = getComputedStyle(i, '::before').content; return !c || c === 'none' || c === 'normal' || c === '""'; });
            add('T10', 'Share button icons render', bad.length ? 'FAIL' : 'PASS', `${bad.length} missing (${bad.map((i) => i.className).join(' ')})`, '0 missing',
                bad.length ? [tag(bad[0].closest('.social-share-container') || bad[0], 'T10')] : []);
        }
    }

    // T11 is run from Node (needs scrolling) — see tocCheck()

    // T12 — themed checkboxes
    {
        const boxes = [...document.querySelectorAll('.checklist-container input[type="checkbox"]')];
        if (!boxes.length) NA('T12', 'Checkbox styling', 'no checklist');
        else {
            const s = getComputedStyle(boxes[0]);
            const ok = (s.accentColor && s.accentColor !== 'auto') || s.appearance === 'none';
            add('T12', 'Checkboxes match theme', ok ? 'PASS' : 'FAIL', `accent-color ${s.accentColor}, appearance ${s.appearance}`, 'accent colour set', ok ? [] : [tag(boxes[0].closest('label'), 'T12')]);
        }
    }

    // T13 — faint oversized watermark icons behind text
    {
        const marks = [...content.querySelectorAll('*')].filter((e) => { const s = getComputedStyle(e); return parseFloat(s.opacity) <= 0.05 && parseFloat(s.fontSize) >= 64 && visible(e); });
        add('T13', 'No watermark icons behind text', marks.length ? 'FAIL' : 'PASS', `${marks.length} found`, '0', marks.slice(0, 1).map((e) => tag(e.parentElement, 'T13')));
    }

    // T14 — footer centred
    {
        const p = document.querySelector('footer .container > p');
        const s = document.querySelector('footer .social-links');
        if (!p || !s) NA('T14', 'Footer alignment', 'footer not found');
        else {
            const range = document.createRange(); range.selectNodeContents(p);
            const tr = range.getBoundingClientRect();
            const sr = [...s.children].map((c) => c.getBoundingClientRect());
            const socialMid = (Math.min(...sr.map((r) => r.left)) + Math.max(...sr.map((r) => r.right))) / 2;
            const diff = Math.abs((tr.left + tr.width / 2) - socialMid);
            add('T14', 'Footer text and icons centred', diff <= 4 ? 'PASS' : 'FAIL', `${Math.round(diff)}px off-centre`, '≤4px', diff <= 4 ? [] : [tag(document.querySelector('footer'), 'T14')]);
        }
    }

    // T15 — opening paragraph length
    {
        const lead = document.querySelector('.lead');
        if (!lead) NA('T15', 'Opening paragraph', 'no .lead');
        else {
            const n = lines(lead);
            const limit = vp === 'desktop' ? 5 : 6;
            add('T15', 'Opening paragraph length', n <= limit ? 'PASS' : 'FAIL', `${n} lines at ${getComputedStyle(lead).fontSize}`, `≤${limit} lines`, n <= limit ? [] : [tag(lead, 'T15')]);
        }
    }

    // T16 — stat tiles compact
    {
        const labels = [...document.querySelectorAll('.stat-tile .stat-label')];
        if (!labels.length) NA('T16', 'Stat tiles', 'no stat tiles');
        else if (vp === 'desktop') {
            const maxL = Math.max(...labels.map(lines));
            add('T16', 'Stat tile labels short', maxL <= 3 ? 'PASS' : 'FAIL', `longest label ${maxL} lines`, '≤3 lines', maxL <= 3 ? [] : [tag(labels.find((l) => lines(l) === maxL).closest('.stat-trio'), 'T16')]);
        } else {
            const quads = [...document.querySelectorAll('.stat-quad')];
            if (!quads.length) NA('T16', 'Stat tiles (mobile 2-up)', 'no 4-tile block');
            else {
                const cols = Math.min(...quads.map((q) => new Set([...q.children].map((c) => Math.round(c.getBoundingClientRect().left))).size));
                add('T16', 'Four-tile blocks show 2 per row on phone', cols >= 2 ? 'PASS' : 'FAIL', `${cols} per row`, '2 per row', cols >= 2 ? [] : [tag(quads[0], 'T16')]);
            }
        }
    }

    // T17 — gap between hero tags and the opening paragraph
    {
        const tags = document.querySelector('.blog-post-tags');
        const lead = document.querySelector('.lead');
        if (!tags || !lead) NA('T17', 'Hero-to-article gap', 'hero or lead missing');
        else {
            const gap = Math.round(lead.getBoundingClientRect().top - tags.getBoundingClientRect().bottom);
            const limit = vp === 'desktop' ? 120 : 96;
            add('T17', 'Hero-to-article gap', gap <= limit ? 'PASS' : 'FAIL', `${gap}px`, `≤${limit}px`);
        }
    }

    // T18 — headings with a single orphaned word on the last line
    {
        const bad = [...content.querySelectorAll('h2, h3')].filter((h) => {
            const w = lineRects(h);
            return w.length > 1 && w[w.length - 1] < 0.25 * w[0];
        });
        add('T18', 'No orphaned words in headings', bad.length ? 'FAIL' : 'PASS', bad.length ? `${bad.length}: "${bad[0].textContent.trim()}"` : 'none', '0', bad.slice(0, 2).map((e) => tag(e, 'T18')));
    }

    // T19 — author note uses the width on phones
    {
        const p = [...content.querySelectorAll('p')].find((x) => x.textContent.trim().startsWith('Written by'));
        if (!p) NA('T19', 'Author note width', 'no author note');
        else {
            const box = p.parentElement;
            const ratio = p.getBoundingClientRect().width / box.getBoundingClientRect().width;
            const ok = vp === 'desktop' || ratio >= 0.8;
            add('T19', 'Author note uses card width', ok ? 'PASS' : 'FAIL', `text uses ${Math.round(ratio * 100)}% of card`, vp === 'desktop' ? 'info only' : '≥80%', ok ? [] : [tag(box, 'T19')]);
        }
    }

    // T20 — particles not visible through article text
    {
        const canvas = document.getElementById('particles-canvas');
        if (!canvas) NA('T20', 'Particles behind text', 'no particle canvas');
        else {
            const cs = getComputedStyle(canvas);
            const hidden = cs.display === 'none' || parseFloat(cs.opacity) === 0;
            const bg = rgba(getComputedStyle(content).backgroundColor);
            const shielded = bg[3] >= 0.85;
            add('T20', 'Particles hidden behind article text', hidden || shielded ? 'PASS' : 'FAIL',
                hidden ? 'canvas hidden' : `article background alpha ${bg[3]}, canvas opacity ${cs.opacity}`, 'article bg alpha ≥0.85 or canvas hidden');
        }
    }
    return out;
}

// T11 — contents sidebar highlights the section in view (desktop only; sidebar hidden <1200px)
async function tocCheck(page, vp) {
    if (vp !== 'desktop') return { id: 'T11', title: 'Contents sidebar tracks position', status: 'N/A', value: 'sidebar hidden on mobile', target: '-', offenders: [] };
    const hrefs = await page.$$eval('.toc-link', (ls) => ls.map((l) => l.getAttribute('href')));
    if (!hrefs.length) return { id: 'T11', title: 'Contents sidebar tracks position', status: 'N/A', value: 'no sidebar', target: '-', offenders: [] };
    const wrong = [];
    for (const h of hrefs) {
        await page.evaluate((sel) => {
            const el = document.querySelector(sel);
            if (el) window.scrollTo(0, el.getBoundingClientRect().top + window.scrollY - 150);
        }, h);
        await page.waitForTimeout(350);
        const active = await page.$eval('.toc-link.active', (a) => a.getAttribute('href')).catch(() => null);
        if (active !== h) wrong.push(`${h}→${active || 'none'}`);
    }
    await page.evaluate(() => window.scrollTo(0, document.body.scrollHeight));
    await page.waitForTimeout(400);
    const atBottom = await page.$eval('.toc-link.active', (a) => a.getAttribute('href')).catch(() => null);
    if (atBottom !== hrefs[hrefs.length - 1]) wrong.push(`page bottom→${atBottom || 'none'}`);
    const total = hrefs.length + 1;
    return {
        id: 'T11', title: 'Contents sidebar tracks position', status: wrong.length ? 'FAIL' : 'PASS',
        value: `${total - wrong.length}/${total} correct${wrong.length ? ` (e.g. ${wrong.slice(0, 2).join(', ')})` : ''}`, target: `${total}/${total}`, offenders: [],
    };
}

// ---------- runner ----------
async function auditOne(browser, target, outDir, { screenshots = true } = {}) {
    const vps = VIEWPORT_SEL === 'both' ? ['desktop', 'mobile'] : [VIEWPORT_SEL];
    const results = {};
    for (const vp of vps) {
        const ctx = await browser.newContext(VIEWPORTS[vp]);
        const page = await ctx.newPage();
        const errors = [];
        const failedReq = [];
        page.on('pageerror', (e) => errors.push(e.message));
        page.on('response', (r) => { if (r.status() >= 400 && !IGNORED_REQUEST_HOSTS.some((h) => r.url().includes(h))) failedReq.push(`${r.status()} ${r.url()}`); });
        page.on('requestfailed', (r) => {
            const err = (r.failure() && r.failure().errorText) || '';
            // ERR_ABORTED = the browser cancelled it (e.g. a video range request), not a broken asset.
            if (err.includes('ERR_ABORTED') || r.url().startsWith('data:') || IGNORED_REQUEST_HOSTS.some((h) => r.url().includes(h))) return;
            failedReq.push(`failed ${r.url()} (${err})`);
        });
        await page.goto(target.url, { waitUntil: 'networkidle', timeout: 60000 }).catch(() => page.waitForLoadState('load'));
        await page.addStyleTag({ content: 'html{scroll-behavior:auto!important}' });
        await page.waitForTimeout(1200);

        let checks = await page.evaluate(pageChecks, vp);
        checks.push(await tocCheck(page, vp));
        checks.push({
            id: 'T21', title: 'No script errors or broken assets', status: errors.length || failedReq.length ? 'FAIL' : 'PASS',
            value: `${errors.length} script errors, ${failedReq.length} failed requests${failedReq.length ? ` (${failedReq[0]})` : ''}${errors.length ? ` (${errors[0].slice(0, 80)})` : ''}`,
            target: '0 / 0', offenders: [],
        });
        checks.sort((a, b) => a.id.localeCompare(b.id));
        if (ONLY) checks = checks.filter((c) => ONLY.includes(c.id));

        if (screenshots) {
            const shotDir = path.join(outDir, vp);
            fs.mkdirSync(shotDir, { recursive: true });
            for (const c of checks) {
                c.shots = [];
                if (c.status === 'PASS' || c.status === 'N/A') continue;
                for (const key of c.offenders || []) {
                    const file = path.join(shotDir, `${key}.png`);
                    const loc = page.locator(`[data-audit-id="${key}"]`);
                    try {
                        await loc.scrollIntoViewIfNeeded();
                        await loc.screenshot({ path: file, timeout: 5000 });
                        c.shots.push(path.relative(outDir, file).replace(/\\/g, '/'));
                    } catch { /* element not screenshot-able (e.g. zero height) */ }
                }
            }
            if (flag('slices')) {
                const h = VIEWPORTS[vp].viewport.height;
                const total = await page.evaluate(() => document.body.scrollHeight);
                let i = 0;
                for (let y = 0; y < total; y += h - 60) {
                    await page.evaluate((yy) => window.scrollTo(0, yy), y);
                    await page.waitForTimeout(250);
                    await page.screenshot({ path: path.join(shotDir, `slice-${String(i++).padStart(2, '0')}.png`) });
                }
            }
        }
        results[vp] = checks;
        await ctx.close();
    }
    return results;
}

const ICON = { PASS: '✅', FAIL: '❌', WARN: '⚠️', 'N/A': '➖' };

function merge(results) {
    const ids = [...new Set(Object.values(results).flat().map((c) => c.id))].sort();
    return ids.map((id) => {
        const d = (results.desktop || []).find((c) => c.id === id);
        const m = (results.mobile || []).find((c) => c.id === id);
        return { id, title: (d || m).title, d, m };
    });
}

function writeReport(target, results, outDir) {
    const rows = merge(results);
    const cell = (c) => (c ? `${ICON[c.status]} ${c.status}` : '—');
    let md = `# Visual audit: ${target.name}\n\n`;
    md += `- Source: \`${target.mode}\` — ${target.url}\n- Run: ${new Date().toISOString()}\n- Viewports: desktop 1440×900, mobile 390×844\n\n`;
    md += '| ID | Check | Desktop | Mobile | Desktop value | Mobile value | Target |\n|---|---|---|---|---|---|---|\n';
    for (const r of rows) {
        md += `| ${r.id} | ${r.title} | ${cell(r.d)} | ${cell(r.m)} | ${r.d ? r.d.value : '—'} | ${r.m ? r.m.value : '—'} | ${(r.d || r.m).target} |\n`;
    }
    const shots = rows.flatMap((r) => ['d', 'm'].flatMap((k) => (r[k] && r[k].shots ? r[k].shots.map((s) => ({ id: r.id, vp: k === 'd' ? 'desktop' : 'mobile', s })) : [])));
    if (shots.length) {
        md += '\n## Screenshots of failures\n\n';
        for (const x of shots) md += `**${x.id} — ${x.vp}**\n\n![${x.id} ${x.vp}](${x.s})\n\n`;
    }
    fs.writeFileSync(path.join(outDir, 'report.md'), md);
    fs.writeFileSync(path.join(outDir, 'results.json'), JSON.stringify({ target, results }, null, 2));
    return rows;
}

function printTable(name, rows) {
    console.log(`\n${name}`);
    console.log('ID   Desktop  Mobile   Check');
    for (const r of rows) {
        const s = (c) => (c ? c.status : '-').padEnd(8);
        console.log(`${r.id}  ${s(r.d)} ${s(r.m)} ${r.title}${[r.d, r.m].some((c) => c && c.status === 'FAIL') ? `  ← ${[r.d, r.m].filter((c) => c && c.status === 'FAIL').map((c) => c.value).join(' | ')}` : ''}`);
    }
}

(async () => {
    const browser = await chromium.launch();
    let anyFail = false;
    try {
        if (flag('all')) {
            const files = fs.readdirSync(BLOG_DIR).filter((f) => f.endsWith('.html') && f !== 'index.html').sort();
            const outDir = opt('out', path.join(__dirname, 'reports', '_all', `${stamp}-${LIVE ? 'live' : 'local'}`));
            fs.mkdirSync(outDir, { recursive: true });
            const summary = [];
            for (const f of files) {
                const target = resolveTarget(f);
                process.stdout.write(`auditing ${f} … `);
                const res = await auditOne(browser, target, path.join(outDir, target.name), { screenshots: false });
                const rows = merge(res);
                const fails = rows.filter((r) => [r.d, r.m].some((c) => c && c.status === 'FAIL')).map((r) => r.id);
                if (fails.length) anyFail = true;
                summary.push({ post: target.name, fails });
                console.log(fails.length ? `FAIL ${fails.join(',')}` : 'PASS');
            }
            let md = `# Visual audit — all posts (${LIVE ? 'live' : 'local'})\n\nRun: ${new Date().toISOString()}\n\n| Post | Failing checks |\n|---|---|\n`;
            for (const s of summary) md += `| ${s.post} | ${s.fails.length ? s.fails.join(', ') : '✅ none'} |\n`;
            const counts = {};
            summary.forEach((s) => s.fails.forEach((id) => { counts[id] = (counts[id] || 0) + 1; }));
            md += `\n## Posts failing each check\n\n| Check | Posts |\n|---|---|\n${Object.entries(counts).sort().map(([k, v]) => `| ${k} | ${v} |`).join('\n')}\n`;
            fs.writeFileSync(path.join(outDir, 'summary.md'), md);
            console.log(`\nSummary: ${path.relative(REPO, path.join(outDir, 'summary.md'))}`);
        } else {
            if (!positional.length) {
                console.error('Usage: node tools/qa/blog-visual-audit.js <post|url> [--live] [--viewport=both] [--only=T01,T02] [--slices]');
                process.exit(2);
            }
            for (const t of positional) {
                const target = resolveTarget(t);
                const outDir = opt('out', path.join(__dirname, 'reports', target.name, `${stamp}-${target.mode}`));
                fs.mkdirSync(outDir, { recursive: true });
                const res = await auditOne(browser, target, outDir);
                const rows = writeReport(target, res, outDir);
                printTable(`${target.name} (${target.mode})`, rows);
                if (rows.some((r) => [r.d, r.m].some((c) => c && c.status === 'FAIL'))) anyFail = true;
                console.log(`\nReport: ${path.relative(REPO, path.join(outDir, 'report.md'))}`);
            }
        }
    } finally {
        await browser.close();
    }
    process.exit(anyFail ? 1 : 0);
})();

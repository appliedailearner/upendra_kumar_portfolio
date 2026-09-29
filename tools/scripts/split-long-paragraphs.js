/**
 * split-long-paragraphs.js — PDCA Cycle 3: break up text walls without rewording.
 *
 *   node tools/scripts/split-long-paragraphs.js <post> [<post> …]   # dry run
 *   node tools/scripts/split-long-paragraphs.js --all [--write]
 *
 * Measures posts at desktop width (1440px), like the audit:
 *   T06  body paragraphs (direct children of the article) over 4 lines are split
 *        at the sentence boundary nearest the middle; repeated until they fit.
 *   T15  an opening .lead over 5 lines keeps its first sentence(s) and the rest
 *        moves into a normal paragraph right after it.
 *
 * Only splits at ". ", "! " or "? " followed by a capital, only where no inline
 * tag (<a>, <strong>, <em>, <span>, …) is open, and only when the sentence text
 * is found exactly once in the source. Anything else is reported and skipped.
 */
const fs = require('fs');
const path = require('path');
const { pathToFileURL } = require('url');
const { chromium } = require('playwright-chromium');

const BLOG = path.join(__dirname, '..', '..', 'site', 'blog');
const args = process.argv.slice(2);
const WRITE = args.includes('--write');
const posts = args.includes('--all')
    ? fs.readdirSync(BLOG).filter((f) => f.endsWith('.html') && !['index.html', 'test-sync-ok.html'].includes(f))
    : args.filter((a) => !a.startsWith('--')).map((p) => (p.endsWith('.html') ? p : `${p}.html`));

const ENTITIES = {
    amp: '&', lt: '<', gt: '>', quot: '"', apos: "'", nbsp: ' ', mdash: '—', ndash: '–', rsquo: '’', lsquo: '‘',
    ldquo: '“', rdquo: '”', hellip: '…', rarr: '→', larr: '←', times: '×', trade: '™', reg: '®', copy: '©', bull: '•',
    middot: '·', deg: '°', plusmn: '±', le: '≤', ge: '≥', ne: '≠', asymp: '≈', euro: '€', pound: '£', minus: '−', check: '✓',
};
const INLINE = /<\/?(a|strong|em|b|i|span|code|mark|abbr|sup|sub|u|small|kbd|q|cite|time)\b[^>]*>/gi;

// Plain-text view of the HTML with a map back to source offsets; whitespace collapsed to one space.
function textView(html) {
    let text = '';
    const map = [];
    let i = 0;
    let lastSpace = true;
    const push = (ch, at) => {
        if (/\s/.test(ch)) { if (lastSpace) return; ch = ' '; lastSpace = true; } else lastSpace = false;
        text += ch; map.push(at);
    };
    const skipBlock = (tag) => { const end = html.indexOf(`</${tag}>`, i); i = end < 0 ? html.length : end + tag.length + 3; };
    while (i < html.length) {
        const c = html[i];
        if (c === '<') {
            if (/^<script\b/i.test(html.slice(i, i + 8))) { skipBlock('script'); continue; }
            if (/^<style\b/i.test(html.slice(i, i + 7))) { skipBlock('style'); continue; }
            if (html.startsWith('<!--', i)) { const e = html.indexOf('-->', i); i = e < 0 ? html.length : e + 3; continue; }
            const e = html.indexOf('>', i);
            i = e < 0 ? html.length : e + 1;
            continue;
        }
        if (c === '&') {
            const m = html.slice(i, i + 12).match(/^&(#x[0-9a-f]+|#\d+|[a-z]+);/i);
            if (m) {
                const n = m[1];
                const ch = n[0] === '#' ? String.fromCodePoint(n[1] === 'x' || n[1] === 'X' ? parseInt(n.slice(2), 16) : parseInt(n.slice(1), 10)) : (ENTITIES[n] || '\u0000');
                push(ch, i);
                i += m[0].length;
                continue;
            }
        }
        push(c, i);
        i++;
    }
    return { text, map };
}

const collapse = (s) => s.replace(/\s+/g, ' ');

function sentenceBoundaries(text) {
    const out = [];
    const re = /[.!?][”"’)]?\s+(?=[A-Z“"‘(0-9])/g;
    let m;
    while ((m = re.exec(text))) {
        const before = text.slice(Math.max(0, m.index - 4), m.index + 1);
        if (/\b(e\.g|i\.e|vs|etc|Mr|Dr|St|approx|incl)\.$/i.test(before) || /\b[A-Z]\.$/.test(before)) continue; // abbreviations
        out.push(m.index + m[0].trimEnd().length); // index just after the punctuation (and closing quote)
    }
    return out;
}

// Split the paragraph whose text is `ptext` at text offset `cut` (just after a sentence's punctuation).
function splitInSource(html, ptext, cut, newTagFor) {
    const view = textView(html);
    const before = collapse(ptext.slice(Math.max(0, cut - 70), cut)).trimStart();
    const after = collapse(ptext.slice(cut, cut + 25)).trimEnd();
    const needle = before + after;
    const first = view.text.indexOf(needle);
    if (first < 0) return { html, why: 'text not found in source' };
    if (view.text.indexOf(needle, first + 1) >= 0) return { html, why: 'text found more than once' };
    const srcCut = view.map[first + before.length - 1] + 1; // just after the punctuation
    // Advance over an entity used as the last char (e.g. &rdquo;)
    let at = srcCut;
    if (html[view.map[first + before.length - 1]] === '&') at = html.indexOf(';', view.map[first + before.length - 1]) + 1;
    const pStart = html.lastIndexOf('<p', at);
    if (pStart < 0 || !/^<p[\s>]/.test(html.slice(pStart, pStart + 3)) || html.slice(pStart, at).includes('</p>')) return { html, why: 'not inside a <p>' };
    const segment = html.slice(html.indexOf('>', pStart) + 1, at);
    let depth = 0;
    for (const t of segment.match(INLINE) || []) depth += t[1] === '/' ? -1 : 1;
    if (depth !== 0) return { html, why: 'inside an inline tag' };
    const openTag = html.slice(pStart, html.indexOf('>', pStart) + 1);
    const lineStart = html.lastIndexOf('\n', pStart) + 1;
    const indent = html.slice(lineStart, pStart).match(/^[ \t]*/)[0];
    const eol = html.includes('\r\n') ? '\r\n' : '\n';
    let rest = at;
    while (/[ \t\r\n]/.test(html[rest])) rest++;
    return { html: `${html.slice(0, at)}</p>${eol}${eol}${indent}${newTagFor(openTag)}${html.slice(rest)}` };
}

(async () => {
    const browser = await chromium.launch();
    const page = await browser.newPage({ viewport: { width: 1440, height: 900 } });
    const summary = [];
    for (const post of posts) {
        const file = path.join(BLOG, post);
        let html = fs.readFileSync(file, 'utf8');
        const original = html;
        const notes = [];
        for (let pass = 0; pass < 4; pass++) {
            if (pass > 0 || html !== fs.readFileSync(file, 'utf8')) {
                const tmp = path.join(BLOG, `.__split-${post}`);
                fs.writeFileSync(tmp, html);
                await page.goto(pathToFileURL(tmp).href, { waitUntil: 'load' }).catch(() => {});
                fs.unlinkSync(tmp);
            } else {
                await page.goto(pathToFileURL(file).href, { waitUntil: 'load' }).catch(() => {});
            }
            await page.waitForTimeout(300);
            let leadLimit = 5;
            const measure = () => page.evaluate((leadLimit) => {
                const content = document.querySelector('.blog-post-content') || document.querySelector('.blog-content');
                if (!content) return [];
                const lines = (el) => {
                    const walker = document.createTreeWalker(el, NodeFilter.SHOW_TEXT);
                    const rects = [];
                    for (let n = walker.nextNode(); n; n = walker.nextNode()) {
                        if (!n.textContent.trim()) continue;
                        const r = document.createRange(); r.selectNodeContents(n);
                        for (const x of r.getClientRects()) if (x.width > 1 && x.height > 1) rects.push(x);
                    }
                    rects.sort((a, b) => a.top - b.top);
                    let count = 0, lastBottom = -1e9;
                    for (const x of rects) if (x.top >= lastBottom - 0.5 * x.height) { count++; lastBottom = x.bottom; } else lastBottom = Math.max(lastBottom, x.bottom);
                    return count;
                };
                const out = [];
                const lead = document.querySelector('.lead');
                if (lead && lines(lead) > leadLimit) out.push({ kind: 'lead', text: lead.textContent, lines: lines(lead) });
                for (const p of content.querySelectorAll(':scope > p')) {
                    if (p.classList.contains('lead') || !p.getBoundingClientRect().width) continue;
                    const n = lines(p);
                    if (n > 4) out.push({ kind: 'body', text: p.textContent, lines: n });
                }
                return out;
            }, leadLimit);
            leadLimit = 5;
            await page.setViewportSize({ width: 1440, height: 900 });
            const targets = await measure();
            // T15 on phones: the opening may be ≤5 lines on desktop but over 6 at 390px
            if (!targets.some((t) => t.kind === 'lead')) {
                await page.setViewportSize({ width: 390, height: 844 });
                await page.waitForTimeout(200);
                leadLimit = 6;
                const mobileLead = (await measure()).filter((t) => t.kind === 'lead');
                targets.unshift(...mobileLead.map((t) => ({ ...t, limit: 6 })));
                await page.setViewportSize({ width: 1440, height: 900 });
            }
            if (!targets.length) break;
            let changed = false;
            for (const t of targets) {
                const bounds = sentenceBoundaries(t.text);
                if (!bounds.length) { notes.push(`skip (${t.kind}, ${t.lines} lines): one sentence — "${collapse(t.text).trim().slice(0, 50)}…"`); continue; }
                const len = t.text.length;
                const goal = t.kind === 'lead' ? len * Math.min(0.5, ((t.limit || 5) - 0.5) / t.lines) : len / 2;
                const pick = t.kind === 'lead'
                    ? (bounds.filter((b) => b <= goal).pop() || bounds[0])
                    : bounds.reduce((a, b) => (Math.abs(b - goal) < Math.abs(a - goal) ? b : a));
                const r = splitInSource(html, t.text, pick, (open) => (t.kind === 'lead' ? '<p>' : open));
                if (r.why) { notes.push(`skip (${t.kind}, ${t.lines} lines): ${r.why} — "${collapse(t.text).trim().slice(0, 50)}…"`); continue; }
                html = r.html;
                changed = true;
                notes.push(`split ${t.kind} (${t.lines} lines) after "…${collapse(t.text.slice(Math.max(0, pick - 40), pick)).trim()}"`);
            }
            if (!changed) break;
        }
        if (html !== original) {
            summary.push(post);
            if (WRITE) fs.writeFileSync(file, html);
        }
        if (notes.length) console.log(`${WRITE && html !== original ? 'patched' : 'post'}  ${post}\n    ${notes.join('\n    ')}`);
    }
    await browser.close();
    console.log(`\n${WRITE ? 'Changed' : 'Would change'} ${summary.length} post(s).${WRITE ? '' : ' Re-run with --write to apply.'}`);
})();

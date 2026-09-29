/**
 * exec-grid-to-rows.js — PDCA Cycle 3 (T03): convert the old 3-column executive summary
 * (`.executive-grid` of `.glass-card`s) into full-width `.exec-rows`, as done by hand in C1-01.
 *
 *   node tools/scripts/exec-grid-to-rows.js            # dry run
 *   node tools/scripts/exec-grid-to-rows.js --write
 *
 * Keeps each card's icon, heading and paragraph HTML exactly; takes the accent colour from
 * the icon and the heading colour from the <h4>. The `.exec-row` styles live in premium.css.
 */
const fs = require('fs');
const path = require('path');

const BLOG = path.join(__dirname, '..', '..', 'site', 'blog');
const WRITE = process.argv.includes('--write');

// Balanced <div> block starting at `start`; returns the index just after its closing tag.
function blockEnd(html, start) {
    const re = /<\/?div\b/g;
    re.lastIndex = start;
    let depth = 0, m;
    while ((m = re.exec(html))) {
        depth += m[0] === '<div' ? 1 : -1;
        if (depth === 0) return html.indexOf('>', m.index) + 1;
    }
    return -1;
}

function cards(grid) {
    const out = [];
    let at = 0;
    for (;;) {
        const s = grid.indexOf('<div class="glass-card"', at);
        if (s < 0) break;
        const e = blockEnd(grid, s);
        out.push(grid.slice(s, e));
        at = e;
    }
    return out;
}

const color = (styleAttr) => ((styleAttr || '').match(/(?:^|;)\s*color:\s*(#[0-9a-fA-F]{3,6})/) || [])[1];

let changed = 0;
for (const f of fs.readdirSync(BLOG).filter((x) => x.endsWith('.html'))) {
    const file = path.join(BLOG, f);
    const html = fs.readFileSync(file, 'utf8');
    const start = html.indexOf('<div class="executive-grid">');
    if (start < 0) continue;
    const end = blockEnd(html, start);
    const eol = html.includes('\r\n') ? '\r\n' : '\n';
    const lineStart = html.lastIndexOf('\n', start) + 1;
    const indent = html.slice(lineStart, start);
    const rows = [];
    let ok = true;
    for (const card of cards(html.slice(start, end))) {
        const icon = card.match(/<i class="(fa[sbr]? fa-[\w-]+)"([^>]*)>/);
        const h4 = card.match(/<h4\b([^>]*)>([\s\S]*?)<\/h4>/);
        const ps = [...card.matchAll(/<p\b[^>]*>([\s\S]*?)<\/p>/g)].map((m) => m[1].trim());
        if (!icon || !h4 || !ps.length) { ok = false; break; }
        const accent = color((icon[2].match(/style="([^"]*)"/) || [])[1]) || '#60a5fa';
        const accentText = color((h4[1].match(/style="([^"]*)"/) || [])[1]) || accent;
        const i2 = `${indent}        `;
        rows.push([
            `${indent}    <div class="exec-row" style="--accent: ${accent}; --accent-text: ${accentText};">`,
            `${indent}        <div class="exec-icon"><i class="${icon[1]}"></i></div>`,
            `${i2}<div>`,
            `${i2}    <h4>${h4[2].trim()}</h4>`,
            ...ps.map((p, n) => `${i2}    <p${n ? ' style="margin-top: 0.6rem;"' : ''}>${p}</p>`),
            `${i2}</div>`,
            `${indent}    </div>`,
        ].join(eol));
    }
    if (!ok || rows.length !== 3) { console.log(`skip  ${f}: unexpected card markup`); continue; }
    const block = `<div class="exec-rows">${eol}${rows.join(eol)}${eol}${indent}</div>`;
    let next = html.slice(0, start) + block + html.slice(end);
    // the grid's own <style> block is now unused
    next = next.replace(/[ \t]*<style>\s*\.executive-grid\s*\{[^}]*\}\s*@media[^{]*\{\s*\.executive-grid\s*\{[^}]*\}\s*\}\s*<\/style>[ \t]*\r?\n/, '');
    changed++;
    console.log(`${WRITE ? 'converted' : 'would convert'}  ${f}  (${rows.length} rows)`);
    if (WRITE) fs.writeFileSync(file, next);
}
console.log(`\n${WRITE ? 'Converted' : 'Would convert'} ${changed} post(s).${WRITE ? '' : ' Re-run with --write to apply.'}`);

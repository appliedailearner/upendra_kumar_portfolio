/**
 * readable-text.js — PDCA Cycle 3 (T09): small and low-contrast text in blog posts.
 *
 *   node tools/scripts/readable-text.js            # dry run
 *   node tools/scripts/readable-text.js --write
 *
 * In every post (inline style="" attributes and the post's own <style> blocks):
 *  - text colours that fall below 4.5:1 contrast on the navy background are swapped for a
 *    lighter shade of the same hue — only the `color:` property, never borders/backgrounds;
 *  - white text on a bright blue/green/purple/amber fill gets the next darker fill shade;
 *  - font sizes under 13px are raised to the caption size (0.85rem / 13px).
 * T07 (type scale): font sizes that apply to paragraphs, list items and table cells — inline
 * style on <p>/<li>/<td>, or post CSS rules whose selector ends in p/li/td — snap to the
 * three-step scale: body 1.15rem, compact 0.95rem, caption 0.85rem. Sizes above 1.3rem
 * (display text) and em-relative sizes are left alone.
 * Inline <svg> is left alone (its text scales with the drawing).
 */
const fs = require('fs');
const path = require('path');

const BLOG = path.join(__dirname, '..', '..', 'site', 'blog');
const WRITE = process.argv.includes('--write');

// dim text colour -> lighter shade of the same hue (contrast on #0f172a)
const COLORS = {
    '#0078d4': '#60a5fa', // Azure blue 3.9 -> 7.0
    '#64748b': '#94a3b8', // slate-500 3.8 -> 7.0
    '#475569': '#94a3b8', // slate-600 2.4 -> 7.0
    '#3b82f6': '#60a5fa', // blue-500 4.0 -> 7.0
    '#a855f7': '#c084fc', // purple-500 3.6 -> 6.3
    '#ef4444': '#f87171', // red-500 4.2 -> 5.9
    'var(--primary-color)': '#60a5fa',
};
// White text on a bright fill (buttons, badges, tabs) -> the next darker shade of the same hue,
// only in a style block that also sets the text white. All give >= 5:1 with white.
const FILLS = {
    '#3b82f6': '#2563eb', // blue 3.7 -> 5.2
    'var(--premium-blue)': '#2563eb',
    '#10b981': '#047857', // green 2.5 -> 5.5
    '#a855f7': '#9333ea', // purple 4.0 -> 5.4
    '#f59e0b': '#b45309', // amber 2.1 -> 5.0
};
const FILL_RE = new RegExp(`(background(?:-color)?\\s*:\\s*)(${Object.keys(FILLS).map((k) => k.replace(/[()-]/g, '\\$&')).join('|')})(?![\\w-])`, 'gi');
const WHITE_TEXT = /(^|[^-\w])color\s*:\s*(white|#fff|#ffffff)\b/i;
const COLOR_RE = new RegExp(`(^|[^-\\w])(color\\s*:\\s*)(${Object.keys(COLORS).map((k) => k.replace(/[()-]/g, '\\$&')).join('|')})(?![\\w-])`, 'gi');
const SIZE_RE = /(font-size\s*:\s*)(\d*\.?\d+)(rem|px)\b/gi;
const MIN = { rem: 0.85, px: 13 }; // 0.85rem = the caption step of the type scale (T07)

// T07: snap a rem/px size onto the scale; null = leave alone
function snap(num, unit) {
    const rem = unit === 'px' ? num / 16 : num;
    if (rem > 1.3 || rem < 0.8) return null;
    const step = rem >= 1.08 ? 1.15 : rem >= 0.86 ? 0.95 : 0.85;
    return Math.abs(step - rem) < 0.001 ? null : `${step}rem`;
}
// uppercase, letter-spaced eyebrow labels are not body text: leave their size alone
const isLabel = (decls) => /text-transform:\s*uppercase/i.test(decls) && /letter-spacing:\s*[\d.]/i.test(decls);
const snapDecls = (decls, bump) => isLabel(decls) ? decls : decls.replace(/(font-size\s*:\s*)(\d*\.?\d+)(rem|px)\b/gi, (m, prop, num, unit) => {
    const s = snap(parseFloat(num), unit.toLowerCase());
    if (!s) return m;
    bump();
    return `${prop}${s}`;
});
const BODY_SELECTOR = /(^|[\s>+~])(p|li|td)(?=$|[.:#[\s])/i;
function typeScale(part, bump) {
    // inline style on <p>, <li>, <td>
    part = part.replace(/<(p|li|td)\b([^>]*?)style="([^"]*)"/gi, (m, tag, pre, style) => `<${tag}${pre}style="${snapDecls(style, bump)}"`);
    // post CSS rules whose (last) selector targets p / li / td
    return part.replace(/(<style\b[^>]*>)([\s\S]*?)(<\/style>)/gi, (m, open, css, close) => open + css.replace(/([^{}]+)\{([^{}]*)\}/g, (rule, sel, decls) => {
        const lastParts = sel.split(',').map((s) => s.trim().split(/\s+/).pop() || '');
        if (!sel.includes('@') && lastParts.some((s) => BODY_SELECTOR.test(` ${s.replace(/::?[\w-]+(\([^)]*\))?/g, '')}`))) return `${sel}{${snapDecls(decls, bump)}}`;
        return rule;
    }) + close);
}

let total = 0;
for (const f of fs.readdirSync(BLOG).filter((x) => x.endsWith('.html') && !['index.html', 'test-sync-ok.html'].includes(x))) {
    const file = path.join(BLOG, f);
    const html = fs.readFileSync(file, 'utf8');
    let colors = 0, sizes = 0, scale = 0, fills = 0;
    // split out inline SVG so it is never touched
    const out = html.split(/(<svg\b[\s\S]*?<\/svg>)/i).map((part) => {
        if (/^<svg\b/i.test(part)) return part;
        return typeScale(part, () => scale++)
            // keep the template's primary-button hover one shade darker than its new base fill
            .replace(/(\.btn-primary:hover\s*\{[^{}]*?background(?:-color)?\s*:\s*)#2563eb/gi, '$1#1d4ed8')
            .replace(COLOR_RE, (m, pre, prop, val) => { colors++; return `${pre}${prop}${COLORS[val.toLowerCase()] || COLORS[val]}`; })
            .replace(/style="[^"]*"|\{[^{}]*\}/g, (block) => !WHITE_TEXT.test(block) ? block
                : block.replace(FILL_RE, (m, prop, val) => { fills++; return `${prop}${FILLS[val.toLowerCase()]}`; }))
            .replace(/style="[^"]*"|\{[^{}]*\}/g, (block) => {
                // Uppercase, letter-spaced labels read fine at 12px (the audit agrees); raising
                // them further widened badges past the phone screen, so their floor is 0.75rem.
                const label = /text-transform:\s*uppercase/i.test(block) && /letter-spacing:\s*[\d.]/i.test(block);
                const min = label ? { rem: 0.75, px: 12 } : MIN;
                return block.replace(SIZE_RE, (m, prop, num, unit) => {
                    const v = parseFloat(num), u = unit.toLowerCase();
                    if (v >= min[u] || v === 0) return m;
                    sizes++;
                    return `${prop}${min[u]}${u}`;
                });
            });
    }).join('');
    if (out !== html) {
        total++;
        console.log(`${WRITE ? 'patched' : 'would patch'}  ${f}: ${colors} colour(s), ${fills} button fill(s), ${sizes} size(s), ${scale} snapped to the type scale`);
        if (WRITE) fs.writeFileSync(file, out);
    }
}
console.log(`\n${WRITE ? 'Patched' : 'Would patch'} ${total} post(s).${WRITE ? '' : ' Re-run with --write to apply.'}`);

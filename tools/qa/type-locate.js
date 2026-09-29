/**
 * type-locate.js — names the elements behind a T07 (type scale) or T09 (small / low-contrast
 * text) failure, so each can be fixed at its source. Uses the same selection rules as
 * blog-visual-audit.js (desktop 1440px).
 *
 *   node tools/qa/type-locate.js <post> [<post> ...]
 */
const path = require('path');
const { pathToFileURL } = require('url');
const { chromium } = require('playwright-chromium');

const BLOG = path.join(__dirname, '..', '..', 'site', 'blog');

function locate() {
    const content = document.querySelector('.blog-post-content') || document.querySelector('.blog-content') || document.body; // .blog-content: two older posts
    const visible = (el) => { const r = el.getBoundingClientRect(); const s = getComputedStyle(el); return r.width > 0 && r.height > 0 && s.visibility !== 'hidden' && s.display !== 'none'; };
    const rgba = (s) => { const m = s.match(/rgba?\(([^)]+)\)/); if (!m) return [0, 0, 0, 0]; const p = m[1].split(/[ ,/]+/).filter(Boolean).map(Number); return [p[0], p[1], p[2], p.length > 3 ? p[3] : 1]; };
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
    const lum = ([r, g, b]) => { const f = (v) => { v /= 255; return v <= 0.03928 ? v / 12.92 : Math.pow((v + 0.055) / 1.055, 2.4); }; return 0.2126 * f(r) + 0.7152 * f(g) + 0.0722 * f(b); };
    const contrast = (a, b) => { const [x, y] = [lum(a), lum(b)].sort((p, q) => q - p); return (x + 0.05) / (y + 0.05); };
    const desc = (e) => {
        const cls = (x) => x && x.className && typeof x.className === 'string' ? `.${x.className.trim().split(/\s+/).join('.')}` : '';
        const st = e.getAttribute('style');
        return `${e.parentElement ? e.parentElement.tagName.toLowerCase() + cls(e.parentElement) + ' > ' : ''}${e.tagName.toLowerCase()}${cls(e)}${st ? ` [style="${st.slice(0, 90)}"]` : ''} "${e.textContent.trim().replace(/\s+/g, ' ').slice(0, 45)}"`;
    };

    const isLabel = (e) => { const cs = getComputedStyle(e); return cs.textTransform === 'uppercase' && parseFloat(cs.letterSpacing) > 0; };
    const els = [...content.querySelectorAll('p, li, td')].filter((e) => visible(e) && !isLabel(e) && !e.closest('.lead, .toc-container, .social-share-container, .stat-tile, .blog-post-meta')
            && parseFloat(getComputedStyle(e).fontSize) <= 20.8); // over 1.3rem = display text (pull quotes), not the body scale
    const bySize = {};
    for (const e of els) (bySize[getComputedStyle(e).fontSize] ||= []).push(e);
    const t07 = Object.entries(bySize).sort((a, b) => parseFloat(b[0]) - parseFloat(a[0]))
        .map(([s, list]) => `  ${s} ×${list.length}\n${list.slice(0, 3).map((e) => `      ${desc(e)}`).join('\n')}`);

    const t09 = [];
    for (const el of content.querySelectorAll('*')) {
        if (!visible(el) || el.closest('.toc-container, svg')) continue;
        if (![...el.childNodes].some((n) => n.nodeType === 3 && n.textContent.trim().length > 1)) continue;
        const s = getComputedStyle(el);
        if (s.webkitTextFillColor && s.webkitTextFillColor.includes('rgba(0, 0, 0, 0)')) continue;
        const fs = parseFloat(s.fontSize);
        const bg = effectiveBg(el);
        const c = bg ? contrast(rgba(s.color), bg) : 21;
        const minSize = s.textTransform === 'uppercase' && parseFloat(s.letterSpacing) > 0 ? 12 : 13;
        if (fs < minSize || c < 4.5) t09.push(`  ${fs}px c=${c.toFixed(1)} color=${s.color} bg=${bg ? bg.slice(0, 3).map(Math.round).join(',') : '?'}  ${desc(el)}`);
    }
    return { t07: Object.keys(bySize).length > 3 ? t07 : [], t09 };
}

(async () => {
    const browser = await chromium.launch();
    const page = await browser.newPage({ viewport: { width: 1440, height: 900 } });
    for (const t of process.argv.slice(2)) {
        const file = path.join(BLOG, t.endsWith('.html') ? t : `${t}.html`);
        await page.goto(pathToFileURL(file).href, { waitUntil: 'load' });
        await page.waitForTimeout(600);
        const r = await page.evaluate(locate);
        console.log(`\n=== ${t}`);
        if (r.t07.length) console.log(` T07:\n${r.t07.join('\n')}`);
        if (r.t09.length) console.log(` T09:\n${r.t09.join('\n')}`);
    }
    await browser.close();
})();

/**
 * find-overflow.js — explain WHY a blog post scrolls sideways (audit check T01).
 *
 *   node tools/qa/find-overflow.js <post> [<post> …] [--width=390]
 *
 * For each post it prints:
 *   1. the page width vs the screen width,
 *   2. elements whose right edge passes the screen and are not inside a scroll box,
 *   3. classes whose elements (or their ::before/::after, e.g. tooltips) make the
 *      page narrower when hidden — this catches culprits that step 2 cannot see.
 */
const path = require('path');
const { pathToFileURL } = require('url');
const { chromium } = require('playwright-chromium');

const args = process.argv.slice(2);
const width = Number((args.find((a) => a.startsWith('--width=')) || '--width=390').split('=')[1]);
const posts = args.filter((a) => !a.startsWith('--')).map((p) => p.replace(/\.html$/, ''));
if (!posts.length) {
    console.error('Usage: node tools/qa/find-overflow.js <post> [<post> …] [--width=390]');
    process.exit(1);
}

(async () => {
    const browser = await chromium.launch();
    for (const post of posts) {
        const page = await browser.newPage({ viewport: { width, height: 900 } });
        const file = path.join(__dirname, '..', '..', 'site', 'blog', `${post}.html`);
        await page.goto(pathToFileURL(file).href, { waitUntil: 'load' }).catch(() => {});
        await page.waitForTimeout(1000);
        const report = await page.evaluate(() => {
            const W = document.documentElement.clientWidth;
            const sw = () => document.documentElement.scrollWidth;
            const base = sw();
            const out = [`page ${base}px, screen ${W}px${base > W ? ` → ${base - W}px too wide` : ' → OK'}`];
            if (base <= W) return out;

            const label = (e) => `${e.tagName.toLowerCase()}${typeof e.className === 'string' && e.className.trim() ? '.' + e.className.trim().split(/\s+/)[0] : ''}`;
            const trail = (e) => { const t = []; for (let a = e; a && a !== document.body && t.length < 3; a = a.parentElement) t.unshift(label(a)); return t.join(' > '); };
            const insideScrollBox = (e) => { for (let a = e.parentElement; a && a !== document.body; a = a.parentElement) if (getComputedStyle(a).overflowX !== 'visible') return true; return false; };

            const off = [...document.querySelectorAll('body *')].filter((e) => {
                if (getComputedStyle(e).position === 'fixed') return false;
                const r = e.getBoundingClientRect();
                return r.width > 0 && r.right > W + 1 && !insideScrollBox(e);
            });
            const set = new Set(off);
            const roots = off.filter((e) => !set.has(e.parentElement));
            out.push('Elements past the screen edge:');
            roots.slice(0, 8).forEach((e) => out.push(`  ${trail(e)}  right=${Math.round(e.getBoundingClientRect().right)}px  "${e.textContent.trim().replace(/\s+/g, ' ').slice(0, 40)}"`));
            if (!roots.length) out.push('  (none — see the class test below)');

            const style = document.createElement('style');
            document.head.appendChild(style);
            const classes = new Set();
            document.querySelectorAll('body [class]').forEach((e) => e.classList.forEach((c) => classes.add(c)));
            const hits = [];
            for (const c of classes) {
                const sel = '.' + CSS.escape(c);
                style.textContent = `${sel}::before,${sel}::after{display:none!important}`;
                const p = sw();
                style.textContent = `${sel}{display:none!important}`;
                const e = sw();
                if (p < base) hits.push(`  ${sel}::before/::after hidden → ${p}px`);
                else if (e < base) hits.push(`  ${sel} hidden → ${e}px`);
            }
            style.remove();
            out.push('Classes that shrink the page when hidden:');
            out.push(...(hits.length ? hits.slice(0, 12) : ['  (none)']));
            return out;
        });
        console.log(`\n${post}\n  ${report.join('\n  ')}`);
        await page.close();
    }
    await browser.close();
})();

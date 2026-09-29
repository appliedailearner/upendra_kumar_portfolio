/**
 * page-speed.js — first paint / first contentful paint / load for pages, median of N runs.
 *
 *   node tools/qa/page-speed.js <url> [<url> …] [--runs=3] [--mobile]
 *
 * Each run uses a fresh browser context (cold cache) and a cache-busting query
 * so Cloudflare serves the current origin copy.
 */
const { chromium } = require('playwright-chromium');

const args = process.argv.slice(2);
const runs = Number((args.find((a) => a.startsWith('--runs=')) || '--runs=3').split('=')[1]);
const mobile = args.includes('--mobile');
const urls = args.filter((a) => !a.startsWith('--'));
const median = (xs) => { const s = [...xs].sort((a, b) => a - b); return s[Math.floor(s.length / 2)]; };

(async () => {
    const browser = await chromium.launch();
    for (const url of urls) {
        const samples = [];
        for (let i = 0; i < runs; i++) {
            const ctx = await browser.newContext(mobile
                ? { viewport: { width: 390, height: 844 }, deviceScaleFactor: 2, isMobile: true, hasTouch: true }
                : { viewport: { width: 1440, height: 900 } });
            const page = await ctx.newPage();
            const u = `${url}${url.includes('?') ? '&' : '?'}cb=${Date.now()}${i}`;
            await page.goto(u, { waitUntil: 'load', timeout: 90000 });
            await page.waitForTimeout(500);
            samples.push(await page.evaluate(() => {
                const nav = performance.getEntriesByType('navigation')[0];
                const paint = Object.fromEntries(performance.getEntriesByType('paint').map((p) => [p.name, p.startTime]));
                return { ttfb: nav.responseStart, fp: paint['first-paint'] || 0, fcp: paint['first-contentful-paint'] || 0, load: nav.loadEventEnd, requests: performance.getEntriesByType('resource').length + 1 };
            }));
            await ctx.close();
        }
        const m = (k) => Math.round(median(samples.map((s) => s[k])));
        console.log(`${url}\n  TTFB ${m('ttfb')}ms  FCP ${m('fcp')}ms  (FCP after TTFB ${m('fcp') - m('ttfb')}ms)  load ${m('load')}ms  requests ${m('requests')}  [median of ${runs}${mobile ? ', mobile' : ''}]`);
    }
    await browser.close();
})();

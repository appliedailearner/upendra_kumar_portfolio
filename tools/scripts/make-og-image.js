/**
 * make-og-image.js — render a 1200x630 social preview image (og:image) for a blog post.
 *
 *   node tools/scripts/make-og-image.js <config.json>
 *
 * config.json:
 *   {
 *     "out": "site/images/blog/<slug>-og.webp",
 *     "eyebrow": "VALUE ARCHITECT PLAYBOOK",
 *     "headline": [["Minutes", "amber"], [" vs. ", "white"], ["Months", "blue"]],
 *     "title": "Closing the SOC Gap in the Age of AI Agents",
 *     "subtitle": "One line under the title.",
 *     "chips": ["Defender XDR", "Sentinel"]
 *   }
 * Colours for headline parts: amber, blue, green, purple, white.
 */
const fs = require('fs');
const path = require('path');
const { chromium } = require('playwright-chromium');
const sharp = require('sharp');

const COLORS = { amber: '#fbbf24', blue: '#38bdf8', green: '#34d399', purple: '#c084fc', white: '#ffffff' };
const esc = (t) => String(t).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');

(async () => {
    const cfgPath = process.argv[2];
    if (!cfgPath) { console.error('usage: node tools/scripts/make-og-image.js <config.json>'); process.exit(1); }
    const c = JSON.parse(fs.readFileSync(cfgPath, 'utf8'));
    const html = `<!doctype html><html><head><meta charset="utf-8"><style>
        * { margin: 0; box-sizing: border-box; }
        body { width: 1200px; height: 630px; overflow: hidden; font-family: 'Segoe UI', system-ui, sans-serif;
               background: radial-gradient(circle at 88% 22%, rgba(126, 34, 206, 0.35) 0, rgba(126, 34, 206, 0) 360px), #0b1120; color: #fff; }
        .wrap { position: absolute; inset: 0; padding: 66px 72px; }
        .eyebrow { color: #34d399; font-size: 20px; font-weight: 700; letter-spacing: 0.22em; }
        .name { position: absolute; top: 74px; right: 72px; color: #94a3b8; font-size: 20px; }
        .headline { margin-top: 22px; font-size: 62px; font-weight: 900; line-height: 1.08; }
        .title { font-size: 54px; font-weight: 900; line-height: 1.12; max-width: 1000px; }
        .sub { margin-top: 24px; color: #94a3b8; font-size: 25px; line-height: 1.4; max-width: 900px; }
        .chips { position: absolute; left: 72px; bottom: 60px; display: flex; gap: 14px; }
        .chip { border: 1px solid rgba(56, 189, 248, 0.45); border-radius: 8px; padding: 13px 18px; font-size: 20px; font-weight: 600; color: #e2e8f0; background: rgba(15, 23, 42, 0.6); }
    </style></head><body><div class="wrap">
        <div class="eyebrow">${esc(c.eyebrow)}</div>
        <div class="name">Upendra Kumar</div>
        <div class="headline">${c.headline.map(([t, col]) => `<span style="color:${COLORS[col] || col}">${esc(t)}</span>`).join('')}</div>
        <div class="title">${esc(c.title)}</div>
        <div class="sub">${esc(c.subtitle)}</div>
        <div class="chips">${c.chips.map((t) => `<div class="chip">${esc(t)}</div>`).join('')}</div>
    </div></body></html>`;
    const browser = await chromium.launch();
    const page = await browser.newPage({ viewport: { width: 1200, height: 630 } });
    await page.setContent(html, { waitUntil: 'load' });
    // fail loudly if the text doesn't fit
    const overflow = await page.evaluate(() => {
        const sub = document.querySelector('.sub').getBoundingClientRect();
        const chips = document.querySelector('.chips').getBoundingClientRect();
        return { overlap: sub.bottom > chips.top - 16, wide: chips.right > 1200 - 40 };
    });
    if (overflow.overlap || overflow.wide) { await browser.close(); throw new Error(`text does not fit: ${JSON.stringify(overflow)}`); }
    const png = await page.screenshot({ type: 'png' });
    await browser.close();
    const out = path.resolve(c.out);
    await sharp(png).webp({ quality: 88 }).toFile(out);
    console.log('wrote', out, fs.statSync(out).size, 'bytes');
})().catch((e) => { console.error(e.message); process.exit(1); });

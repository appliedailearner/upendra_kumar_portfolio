/**
 * patch-blog-template.js — PDCA Cycle 2 per-page edits (see project-docs/BLOG_READABILITY_PDCA_PLAN.md).
 *
 *   node tools/scripts/patch-blog-template.js            # dry run: list what would change
 *   node tools/scripts/patch-blog-template.js --write    # apply
 *
 * Every edit is idempotent, so running it twice changes nothing the second time.
 *   C2-01  Font Awesome 6.4.0 -> 6.5.2 (6.4.0 has no X/Twitter icon), with the matching SRI hash
 *   C2-02  load js/glossary-tidy.js on posts that underline glossary terms
 *   C2-03  load js/toc-tracker.js on posts with a contents sidebar
 *   C2-08  remove the faint oversized watermark icons behind cards (opacity ≤0.05, rem-sized)
 *   C2-10  broken assets: YouTube .webp thumbnails (served only under /vi_webp/), the
 *          Google Fonts "wght=" typo, and LinkedIn post embeds that now return 404
 *          (replaced by a link card to the same post)
 *   CSS    cache-bust premium / dropdown / main stylesheets (all pages) to ?v=56
 */
const fs = require('fs');
const path = require('path');

const SITE = path.join(__dirname, '..', '..', 'site');
const WRITE = process.argv.includes('--write');
const CSS_VERSION = '56';
const FA_OLD = 'font-awesome/6.4.0/css/all.min.css';
const FA_NEW = 'font-awesome/6.5.2/css/all.min.css';
const FA_OLD_SRI = 'sha512-iecdLmaskl7CVkqkXNQ/ZH/XLlvWZOJyj7Yy7tcenmpD1ypASozpmT/E0iPtmFIB46ZmdtAc9eNBvH0H/ZpiBw==';
const FA_NEW_SRI = 'sha512-SnH5WK+bZxgPHs44uWIX+LLJAJ9/2PkPKZ5QiAj6Ta86w+fsb2TkcmfRyVX3pBnMFcV7oQPJkl9QevSCWr3W6A==';
const WATERMARK = /[ \t]*<div\s+style="position: absolute;[^"]*?opacity: 0\.0[1-5]; font-size: \d+(?:\.\d+)?rem;[^"]*">\s*<i class="fas fa-[a-z0-9-]+"><\/i>\s*<\/div>[ \t]*\r?\n/g;
const YT_WEBP = /(?:img\.youtube\.com|i\.ytimg\.com)\/vi\/([\w-]+)\/(\w+default)\.webp/g;
const FONT_TYPO = /family=Outfit:wght=/g;
const LINKEDIN_EMBED = /<iframe\s[^>]*src="https:\/\/www\.linkedin\.com\/embed\/feed\/update\/(urn:li:[a-zA-Z]+:\d+)[^"]*"[^>]*>\s*<\/iframe>/g;
const linkedinCard = (urn) => `<a href="https://www.linkedin.com/feed/update/${urn}/" target="_blank" rel="noopener"
                style="display: inline-flex; align-items: center; gap: 0.75rem; padding: 1rem 1.5rem; border: 1px solid rgba(10, 102, 194, 0.5); border-radius: 12px; background: rgba(10, 102, 194, 0.1); color: #e2e8f0; text-decoration: none; font-weight: 600;">
                <i class="fab fa-linkedin" style="color: #0a66c2; font-size: 1.5rem;"></i> Join the discussion on LinkedIn</a>`;

function htmlFiles(dir) {
    return fs.readdirSync(dir, { withFileTypes: true }).flatMap((d) => {
        const p = path.join(dir, d.name);
        if (d.isDirectory()) return ['node_modules', 'labs'].includes(d.name) ? [] : htmlFiles(p);
        return d.name.endsWith('.html') ? [p] : [];
    });
}

function addScript(html, src) {
    if (html.includes(src)) return html;
    const eol = html.includes('\r\n') ? '\r\n' : '\n';
    const i = html.lastIndexOf('</body>');
    return i < 0 ? html : `${html.slice(0, i)}    <script src="${src}?v=1" defer></script>${eol}${html.slice(i)}`;
}

const totals = {};
const count = (k) => { totals[k] = (totals[k] || 0) + 1; };

for (const file of htmlFiles(SITE)) {
    const rel = path.relative(SITE, file).replace(/\\/g, '/');
    const isPost = rel.startsWith('blog/') && !rel.endsWith('index.html');
    const before = fs.readFileSync(file, 'utf8');
    let html = before;
    const notes = [];

    // CSS cache-bust (all pages: premium and dropdown changed site-wide)
    html = html.replace(/((?:premium|dropdown|main)(?:\.min)?\.css)(\?v=\d+)?"/g, (m, name, v) => {
        if (v === `?v=${CSS_VERSION}`) return m;
        notes.push(`${name}${v || ''} -> ?v=${CSS_VERSION}`); count('css version');
        return `${name}?v=${CSS_VERSION}"`;
    });

    if (isPost) {
        if (html.includes(FA_OLD)) {
            html = html.split(FA_OLD).join(FA_NEW).split(FA_OLD_SRI).join(FA_NEW_SRI);
            notes.push('Font Awesome 6.5.2'); count('C2-01 icons');
        }
        if (/glossaryTerms|class="eli5-term"/.test(html) && !html.includes('glossary-tidy.js')) {
            html = addScript(html, '../js/glossary-tidy.js');
            notes.push('glossary-tidy.js'); count('C2-02 glossary');
        }
        if (/class="[^"]*\btoc-link\b/.test(html) && !html.includes('toc-tracker.js')) {
            html = addScript(html, '../js/toc-tracker.js');
            notes.push('toc-tracker.js'); count('C2-03 contents');
        }
        const marks = (html.match(WATERMARK) || []).length;
        if (marks) {
            html = html.replace(WATERMARK, '');
            notes.push(`${marks} watermark(s) removed`); count('C2-08 watermarks');
        }
        const yt = (html.match(YT_WEBP) || []).length;
        if (yt) {
            html = html.replace(YT_WEBP, 'i.ytimg.com/vi_webp/$1/$2.webp');
            notes.push(`${yt} YouTube thumbnail(s)`); count('C2-10 youtube');
        }
        if (FONT_TYPO.test(html)) {
            html = html.replace(FONT_TYPO, 'family=Outfit:wght@');
            notes.push('Google Fonts URL'); count('C2-10 fonts');
        }
        const li = (html.match(LINKEDIN_EMBED) || []).length;
        if (li) {
            html = html.replace(LINKEDIN_EMBED, (m, urn) => linkedinCard(urn));
            notes.push(`${li} LinkedIn embed(s) -> link card`); count('C2-10 linkedin');
        }
    }

    if (html !== before) {
        console.log(`${WRITE ? 'patched' : 'would patch'}  ${rel}\n    ${notes.join('; ')}`);
        if (WRITE) fs.writeFileSync(file, html);
    }
}

console.log(`\n${WRITE ? 'Applied' : 'Dry run'} — files per change:`);
for (const [k, v] of Object.entries(totals)) console.log(`  ${k}: ${v}`);
if (!WRITE) console.log('\nRe-run with --write to apply.');

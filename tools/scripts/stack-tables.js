/**
 * stack-tables.js — PDCA T04: make a post's tables readable on phones without sideways scroll.
 *
 *   node tools/scripts/stack-tables.js <post> [<post> …]            # dry run
 *   node tools/scripts/stack-tables.js <post> [<post> …] --write
 *
 * For every `<div class="table-scroll">`, adds the `stack-table` class and gives each plain
 * `<td>` a `data-label` taken from its column's `<th>`. On phones premium.css then shows one
 * labelled card per row (see C1-02). Cells that already have attributes are left alone.
 */
const fs = require('fs');
const path = require('path');

const BLOG = path.join(__dirname, '..', '..', 'site', 'blog');
const args = process.argv.slice(2);
const WRITE = args.includes('--write');
const posts = args.filter((a) => !a.startsWith('--')).map((p) => (p.endsWith('.html') ? p : `${p}.html`));
const plain = (s) => s.replace(/<[^>]+>/g, '').replace(/&amp;/g, '&').replace(/&[#\w]+;/g, '').replace(/"/g, '').replace(/\s+/g, ' ').trim();

for (const post of posts) {
    const file = path.join(BLOG, post);
    let html = fs.readFileSync(file, 'utf8');
    let tables = 0, cells = 0;
    html = html.replace(/<div class="table-scroll">([\s\S]*?<\/table>)/g, (block, inner) => {
        const heads = [...inner.matchAll(/<th\b[^>]*>([\s\S]*?)<\/th>/g)].map((m) => plain(m[1]));
        if (!heads.length) return block;
        tables++;
        const body = inner.replace(/<tr>([\s\S]*?)<\/tr>/g, (row, rowInner) => {
            if (!rowInner.includes('<td>')) return row;
            let i = 0;
            return `<tr>${rowInner.replace(/<td>/g, () => { cells++; return `<td data-label="${heads[i++] || ''}">`; })}</tr>`;
        });
        return `<div class="table-scroll stack-table">${body}`;
    });
    console.log(`${WRITE ? 'patched' : 'would patch'}  ${post}: ${tables} table(s), ${cells} cell(s) labelled`);
    if (WRITE && tables) fs.writeFileSync(file, html);
}

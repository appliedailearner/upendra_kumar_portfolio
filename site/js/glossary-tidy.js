/**
 * glossary-tidy.js — keeps glossary underlines readable.
 *
 * Each post's own script wraps glossary terms in <span class="eli5-term">.
 * This runs after it and unwraps the ones that add noise:
 *   - terms inside cards, tables, timelines, callouts or bold text;
 *   - every occurrence of a term after the first one in running text.
 */
(function () {
    var COMPONENTS = [
        '.glass-card', '.mini-card', '.exec-row', '.incident', '.incident-steps', '.step-list',
        '.stat-tile', '.stat-card', '.arch-stack', '.checklist-item', '.checklist-container',
        '.timeline', '.caption', '.sources-box', '.executive-insight', '.toc-container',
        'table', 'strong', 'b', 'summary', 'blockquote'
    ].join(', ');

    function unwrap(span) {
        var parent = span.parentNode;
        while (span.firstChild) parent.insertBefore(span.firstChild, span);
        parent.removeChild(span);
        parent.normalize();
    }

    function tidy() {
        var seen = {};
        var terms = document.querySelectorAll('.eli5-term');
        for (var i = 0; i < terms.length; i++) {
            var term = terms[i];
            var key = term.textContent.trim().toLowerCase();
            if (term.closest(COMPONENTS) || seen[key]) unwrap(term);
            else seen[key] = true;
        }
    }

    // Posts add their underlines on DOMContentLoaded; run after that pass.
    function schedule() { setTimeout(tidy, 0); }
    if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', schedule);
    else schedule();
})();

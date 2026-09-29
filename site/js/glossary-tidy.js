/**
 * glossary-tidy.js — keeps glossary underlines readable.
 *
 * Each post's own script wraps glossary terms in <span class="eli5-term">.
 * This unwraps the ones that add noise:
 *   - terms inside cards, tables, timelines, callouts or bold text;
 *   - every occurrence of a term after the first one in running text.
 *
 * It does not rely on running after the post's script (script order can differ
 * live): it tidies on load and again whenever new terms are added.
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

    var queued = false;
    function schedule() {
        if (queued) return;
        queued = true;
        setTimeout(function () { queued = false; tidy(); }, 0);
    }

    function addsTerms(mutations) {
        for (var i = 0; i < mutations.length; i++) {
            var added = mutations[i].addedNodes;
            for (var j = 0; j < added.length; j++) {
                var n = added[j];
                if (n.nodeType === 1 && (n.classList.contains('eli5-term') || n.querySelector('.eli5-term'))) return true;
            }
        }
        return false;
    }

    new MutationObserver(function (m) { if (addsTerms(m)) schedule(); })
        .observe(document.documentElement, { childList: true, subtree: true });

    if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', schedule);
    else schedule();
    window.addEventListener('load', schedule);
})();

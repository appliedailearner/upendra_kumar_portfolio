/**
 * toc-tracker.js — highlights the contents-sidebar link for the section being read.
 *
 * Rule: the active section is the last heading whose top has scrolled above
 * 160px from the top of the screen; at the bottom of the page it is the last
 * link. Older posts carry their own highlight code (IntersectionObserver
 * variants that miss short sections); if one of those changes the highlight,
 * this script puts the correct one back.
 */
(function () {
    var OFFSET = 160;
    var links = [];
    var targets = [];
    var applying = false;

    function current() {
        var doc = document.documentElement;
        if (window.innerHeight + window.scrollY >= doc.scrollHeight - 2) return links.length - 1;
        // Nearest heading above the line, even if the sidebar lists sections out of page order.
        var idx = 0, best = -Infinity;
        for (var i = 0; i < targets.length; i++) {
            var top = targets[i].getBoundingClientRect().top;
            if (top <= OFFSET && top > best) { best = top; idx = i; }
        }
        return idx;
    }

    function apply() {
        if (!links.length) return;
        var want = current();
        applying = true;
        for (var i = 0; i < links.length; i++) {
            var on = i === want;
            if (links[i].classList.contains('active') !== on) links[i].classList.toggle('active', on);
        }
        applying = false;
    }

    function init() {
        var all = document.querySelectorAll('.toc-link[href^="#"]');
        for (var i = 0; i < all.length; i++) {
            var id = decodeURIComponent(all[i].getAttribute('href').slice(1));
            var el = id && document.getElementById(id);
            if (el) { links.push(all[i]); targets.push(el); }
        }
        if (!links.length) return;

        var queued = false;
        window.addEventListener('scroll', function () {
            if (queued) return;
            queued = true;
            requestAnimationFrame(function () { queued = false; apply(); });
        }, { passive: true });
        window.addEventListener('resize', apply);

        var box = links[0].parentElement;
        while (box && !box.contains(links[links.length - 1])) box = box.parentElement;
        new MutationObserver(function () { if (!applying) apply(); })
            .observe(box || document.body, { subtree: true, attributes: true, attributeFilter: ['class'] });

        apply();
    }

    if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init);
    else init();
})();

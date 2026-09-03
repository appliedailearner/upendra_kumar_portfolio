// Smooth Back Navigation for Case Studies
// This script enhances navigation from case study pages back to the projects page

(function() {
    'use strict';

    // Enhanced Back to Projects Navigation
    function smoothBackToProjects(event) {
        event.preventDefault();
        const targetUrl = event.currentTarget.href;
        
        // Smooth scroll to top first
        window.scrollTo({ top: 0, behavior: 'smooth' });
        
        // Add fade-out effect
        document.body.style.transition = 'opacity 0.3s ease-out';
        document.body.style.opacity = '0';
        
        // Navigate after animation
        setTimeout(() => {
            window.location.href = targetUrl;
        }, 300);
    }

    // Apply smooth navigation to all "Back to Projects" links
    function initSmoothNavigation() {
        document.querySelectorAll('a[href*="projects.html"]').forEach(link => {
            // Only apply to back navigation links, not nav menu
            if (link.textContent.includes('Back to Projects') || link.closest('.cta-button')) {
                link.addEventListener('click', smoothBackToProjects);
                
                // Add visual enhancement - subtle hover effect
                link.style.transition = 'all 0.3s ease';
                link.addEventListener('mouseenter', () => {
                    link.style.transform = 'translateX(-5px)';
                });
                link.addEventListener('mouseleave', () => {
                    link.style.transform = 'translateX(0)';
                });
            }
        });
    }

    // Smooth fade-in on page load
    function initPageTransition() {
        document.body.style.opacity = '0';
        window.addEventListener('load', () => {
            document.body.style.transition = 'opacity 0.3s ease-in';
            document.body.style.opacity = '1';
        });
    }

    // Smooth scroll for TOC links (if present)
    function initSmoothScroll() {
        document.querySelectorAll('.toc-list a, a[href^="#"]').forEach(anchor => {
            anchor.addEventListener('click', function (e) {
                const href = this.getAttribute('href');
                if (href.startsWith('#')) {
                    e.preventDefault();
                    const target = document.querySelector(href);
                    if (target) {
                        target.scrollIntoView({ behavior: 'smooth', block: 'start' });
                    }
                }
            });
        });
    }

    // Initialize all enhancements
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', () => {
            initPageTransition();
            initSmoothNavigation();
            initSmoothScroll();
        });
    } else {
        initPageTransition();
        initSmoothNavigation();
        initSmoothScroll();
    }

})();

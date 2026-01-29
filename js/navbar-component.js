/**
 * Global Navbar Component
 * Injects the standardized Mega-Menu into every page.
 */

document.addEventListener('DOMContentLoaded', () => {
    const navPlaceholder = document.getElementById('dynamic-nav');
    if (!navPlaceholder) return;

    // Detect if we are in a subfolder (blog or pages) to fix relative paths
    const isSubfolder = window.location.pathname.includes('/blog/') || window.location.pathname.includes('/pages/');
    const base = isSubfolder ? '../' : './';

    const navbarHTML = `
    <div class="container">
        <div class="nav-brand" style="display: flex; align-items: center; gap: 1rem;">
            <a href="${base}index.html" style="text-decoration: none;">
                <video autoplay loop muted playsinline class="nav-logo-video">
                    <source src="${base}images/logo-animated.mp4" type="video/mp4">
                </video>
            </a>
            <div>
                <div class="brand-title">Upendra Kumar</div>
                <p class="nav-tagline">Professional Services Delivery Architect</p>
            </div>
        </div>
        <ul class="nav-menu">
            <li><a href="${base}index.html">Home</a></li>
            <li><a href="${base}pages/expertise.html">Expertise</a></li>
            
            <!-- MEGA MENU START -->
            <li class="nav-item-dropdown">
                <a href="${base}blog.html" class="dropdown-trigger" style="display: flex; align-items: center; gap: 6px;">
                    Insights <i class="fas fa-chevron-down" style="font-size: 0.7em; opacity: 0.7;"></i>
                </a>
                <div class="dropdown-menu">
                    <div class="dropdown-content">
                        
                        <!-- Column 1: AI -->
                        <div class="dropdown-column">
                            <h4 class="dropdown-header">🤖 AI Architecture</h4>
                            <a href="${base}blog/2026-01-28-regulator-ready-ai-fortress.html" class="dropdown-link">
                                <i class="fas fa-shield-halved"></i>
                                <span>Regulator-Ready AI Fortress</span>
                            </a>
                            <a href="${base}blog/2026-01-21-uklifelabs-ai-gateway-pattern.html" class="dropdown-link">
                                <i class="fas fa-route"></i>
                                <span>UKLifeLabs AI Gateway</span>
                            </a>
                             <a href="${base}blog/2026-01-11-ai-hosting-decision-tree.html" class="dropdown-link">
                                <i class="fas fa-sitemap"></i>
                                <span>AI Hosting Decision Tree</span>
                            </a>
                        </div>

                        <!-- Column 2: Azure -->
                        <div class="dropdown-column">
                            <h4 class="dropdown-header">☁️ Azure Core</h4>
                            <a href="${base}blog/2026-01-26-hybrid-dns-pattern-cutover-night.html" class="dropdown-link">
                                <i class="fas fa-network-wired"></i>
                                <span>Hybrid DNS Pattern</span>
                            </a>
                            <a href="${base}blog/2025-12-25-azure-landing-zones.html" class="dropdown-link">
                                <i class="fas fa-cloud"></i>
                                <span>Enterprise Landing Zones</span>
                            </a>
                            <a href="${base}blog/2026-01-15-from-tco-to-go-the-wave-1-azure-business-case-playbook.html" class="dropdown-link">
                                <i class="fas fa-chart-pie"></i>
                                <span>The TCO-to-Go Playbook</span>
                            </a>
                        </div>

                        <!-- Column 3: Strategy -->
                        <div class="dropdown-column">
                            <h4 class="dropdown-header">👔 Strategy & Lead</h4>
                            <a href="${base}blog/2026-01-02-value-selling-for-architects.html" class="dropdown-link">
                                <i class="fas fa-sack-dollar"></i>
                                <span>Value-Selling for Architects</span>
                            </a>
                            <a href="${base}blog/2025-12-26-leadership-mental-models.html" class="dropdown-link">
                                <i class="fas fa-brain"></i>
                                <span>Leadership Mental Models</span>
                            </a>
                             <a href="${base}blog/2025-12-07-ticket-solver-to-visionary.html" class="dropdown-link">
                                <i class="fas fa-arrow-up-right-dots"></i>
                                <span>Ticket-Solver to Visionary</span>
                            </a>
                        </div>

                        <div class="dropdown-footer">
                            <a href="${base}blog.html" class="dropdown-footer-link">
                                View Full Library (25+ Articles) <i class="fas fa-arrow-right"></i>
                            </a>
                        </div>
                    </div>
                </div>
            </li>
            <!-- MEGA MENU END -->

            <li><a href="${base}pages/contact.html">Contact</a></li>
            <li class="nav-item">
                <a class="nav-link btn btn-primary text-white ms-lg-3 px-4 shadow-sm rounded-pill flex items-center gap-2"
                    href="${base}assets/pdf/Upendra_Kumar_Resume.pdf" target="_blank"
                    style="line-height: 1.5; font-weight: 600;">
                    <i class="fas fa-file-download"></i> Executive Brief
                </a>
            </li>
        </ul>
        <div class="hamburger ms-auto" aria-label="Toggle navigation" role="button" tabindex="0">
            <span></span>
            <span></span>
            <span></span>
        </div>
    </div>
    `;

    navPlaceholder.innerHTML = navbarHTML;

    // Re-initialize Mobile Hamburger Menu Logic
    const hamburger = navPlaceholder.querySelector('.hamburger');
    const navMenu = navPlaceholder.querySelector('.nav-menu');
    const dropdownTrigger = navPlaceholder.querySelector('.dropdown-trigger');
    const dropdownMenu = navPlaceholder.querySelector('.dropdown-menu');

    if (hamburger) {
        hamburger.addEventListener('click', () => {
            hamburger.classList.toggle('active');
            navMenu.classList.toggle('active');
        });
    }

    // Mobile Dropdown Toggle
    if (dropdownTrigger && window.innerWidth <= 992) {
        dropdownTrigger.addEventListener('click', (e) => {
            e.preventDefault();
            dropdownMenu.style.display = dropdownMenu.style.display === 'block' ? 'none' : 'block';
        });
    }
});

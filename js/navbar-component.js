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
                <a href="${base}blog.html" class="dropdown-trigger" aria-haspopup="true" aria-expanded="false" style="display: flex; align-items: center; gap: 6px;">
                    Insights <i class="fas fa-chevron-down" style="font-size: 0.7em; opacity: 0.7;"></i>
                </a>
                <div class="dropdown-menu">
                    <div class="dropdown-content">
                        
                        <!-- Column 1: Regulator-Ready Series -->
                        <div class="dropdown-column">
                            <h4 class="dropdown-header">🛡️ Regulator-Ready AI</h4>
                            <a href="${base}blog/2026-01-28-regulator-ready-ai-fortress.html" class="dropdown-link">
                                <i class="fas fa-shield-halved"></i>
                                <span>The AI Fortress Blueprint</span>
                            </a>
                            <a href="${base}blog/2026-01-29-architectural-integrity-ai-audit-framework.html" class="dropdown-link">
                                <i class="fas fa-file-contract"></i>
                                <span>The AI Audit Framework</span>
                            </a>
                            <a href="${base}blog/2026-01-21-uklifelabs-ai-gateway-pattern.html" class="dropdown-link">
                                <i class="fas fa-route"></i>
                                <span>AI Gateway Controls</span>
                            </a>
                             <a href="${base}blog/2026-01-11-ai-hosting-decision-tree.html" class="dropdown-link">
                                <i class="fas fa-sitemap"></i>
                                <span>AI Hosting Strategy</span>
                            </a>
                        </div>

                        <!-- Column 2: Migration Chronicles -->
                        <div class="dropdown-column">
                            <h4 class="dropdown-header">🚀 Migration Chronicles</h4>
                            <a href="${base}blog/2026-01-26-hybrid-dns-pattern-cutover-night.html" class="dropdown-link">
                                <i class="fas fa-network-wired"></i>
                                <span>The Hybrid DNS Pattern</span>
                            </a>
                            <a href="${base}blog/2026-01-06-the-bank-that-recalculated-reality.html" class="dropdown-link">
                                <i class="fas fa-university"></i>
                                <span>The Migration That Almost Failed</span>
                            </a>
                            <a href="${base}blog/2025-12-30-azure-migrate-trap.html" class="dropdown-link">
                                <i class="fas fa-triangle-exclamation"></i>
                                <span>The Azure Migrate Trap</span>
                            </a>
                        </div>

                        <!-- Column 3: Value Architect -->
                        <div class="dropdown-column">
                            <h4 class="dropdown-header">🧠 Value Architect Playbook</h4>
                            <a href="${base}blog/2026-02-01-busy-is-not-progress.html" class="dropdown-link">
                                <i class="fas fa-compass"></i>
                                <span>Busy Is Not Progress</span>
                            </a>
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
                    href="${base}assets/downloads/Upendra_Kumar.pdf" target="_blank"
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
    if (dropdownTrigger) {
        dropdownTrigger.addEventListener('click', (e) => {
            if (window.innerWidth <= 992) {
                e.preventDefault();
                const isExpanded = dropdownTrigger.getAttribute('aria-expanded') === 'true';
                dropdownTrigger.setAttribute('aria-expanded', !isExpanded);
                dropdownMenu.style.display = isExpanded ? 'none' : 'block';
            }
        });
    }

    // Reset Dropdown on Resize
    window.addEventListener('resize', () => {
        if (window.innerWidth > 992) {
            dropdownMenu.style.display = ''; // Reset to CSS default
            navMenu.classList.remove('active');
            hamburger.classList.remove('active');
        }
    });
});

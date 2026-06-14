/**
 * Command Palette (Ctrl+K)
 * A power-user navigation tool for the portfolio.
 */
class CommandPalette {
    constructor() {
        this.isOpen = false;
        this.selectedIndex = 0;
        this.items = [];
        this.filteredItems = [];

        this.init();
    }

    init() {
        this.injectHTML();
        this.cacheDOM();
        this.bindEvents();
        this.collectItems();
    }

    injectHTML() {
        const modalHTML = `
            <div id="cmd-overlay" class="cmd-overlay" style="display: none;">
                <div class="cmd-modal">
                    <div class="cmd-header">
                        <i class="fas fa-search cmd-icon"></i>
                        <input type="text" id="cmd-input" placeholder="Type a command or search..." autocomplete="off">
                        <span class="cmd-badge">ESC</span>
                    </div>
                    <div class="cmd-body">
                        <div id="cmd-results" class="cmd-results"></div>
                        <div id="cmd-footer" class="cmd-footer">
                            <div class="cmd-footer-item"><span class="cmd-key">↑↓</span> to navigate</div>
                            <div class="cmd-footer-item"><span class="cmd-key">↵</span> to select</div>
                        </div>
                    </div>
                </div>
            </div>
        `;
        document.body.insertAdjacentHTML('beforeend', modalHTML);
    }

    cacheDOM() {
        this.overlay = document.getElementById('cmd-overlay');
        this.input = document.getElementById('cmd-input');
        this.resultsContainer = document.getElementById('cmd-results');
    }

    bindEvents() {
        // Open/Close
        document.addEventListener('keydown', (e) => {
            if ((e.ctrlKey || e.metaKey) && e.key === 'k') {
                e.preventDefault();
                this.toggle();
            }
            if (e.key === 'Escape' && this.isOpen) {
                this.close();
            }
        });

        // Outside Click
        this.overlay.addEventListener('click', (e) => {
            if (e.target === this.overlay) this.close();
        });

        // Input Handling
        this.input.addEventListener('input', () => {
            this.filterItems(this.input.value);
        });

        this.input.addEventListener('keydown', (e) => {
            if (e.key === 'ArrowDown') {
                e.preventDefault();
                this.navigate(1);
            } else if (e.key === 'ArrowUp') {
                e.preventDefault();
                this.navigate(-1);
            } else if (e.key === 'Enter') {
                e.preventDefault();
                this.selectItem();
            }
        });
    }

    collectItems() {
        // 1. Static Pages (Scraped from typical structure or hardcoded)
        this.items = [
            { category: 'Navigation', title: 'Home', icon: 'fas fa-home', action: () => window.location.href = '/' },
            { category: 'Navigation', title: 'Expertise', icon: 'fas fa-brain', action: () => window.location.href = '/pages/expertise.html' },
            { category: 'Navigation', title: 'Projects', icon: 'fas fa-project-diagram', action: () => window.location.href = '/pages/projects.html' },
            { category: 'Navigation', title: 'Blog', icon: 'fas fa-book', action: () => window.location.href = '/blog.html' },

            // 2. Actions
            { category: 'Actions', title: 'Contact Me', icon: 'fas fa-envelope', action: () => window.location.href = '/#contact' },
            { category: 'Actions', title: 'View Resume', icon: 'fas fa-file-pdf', action: () => window.open('https://portfolio.upendrakumar.com/resume.pdf', '_blank') },
            {
                category: 'Actions', title: 'Copy URL', icon: 'fas fa-link', action: () => {
                    navigator.clipboard.writeText(window.location.href);
                    this.close();
                    alert('URL Copied to clipboard!');
                }
            },

            // 3. Recent/Featured Blogs (Manually Curated for High Impact)
            { category: 'Recent Posts', title: 'Enterprise CRA Playbook', icon: 'fas fa-star', action: () => window.location.href = '/blog/2026-02-12-cloud-readiness-assessment-playbook.html' },
            { category: 'Recent Posts', title: 'TrustBank AI Gateway', icon: 'fas fa-shield-alt', action: () => window.location.href = '/blog/2026-01-09-two-doors-one-rulebook-ai-gateway.html' },
            { category: 'Recent Posts', title: 'The Hybrid DNS Pattern', icon: 'fas fa-network-wired', action: () => window.location.href = '/blog/2026-01-26-hybrid-dns-pattern-cutover-night.html' },
        ];
    }

    toggle() {
        if (this.isOpen) this.close();
        else this.open();
    }

    open() {
        this.isOpen = true;
        this.overlay.style.display = 'flex';
        this.input.value = '';
        this.input.focus();
        this.filterItems('');
        document.body.style.overflow = 'hidden'; // Prevent scrolling
    }

    close() {
        this.isOpen = false;
        this.overlay.style.display = 'none';
        document.body.style.overflow = '';
    }

    filterItems(query) {
        const q = query.toLowerCase();
        this.filteredItems = this.items.filter(item =>
            item.title.toLowerCase().includes(q) ||
            item.category.toLowerCase().includes(q)
        );
        this.selectedIndex = 0;
        this.renderResults();
    }

    renderResults() {
        this.resultsContainer.innerHTML = '';

        if (this.filteredItems.length === 0) {
            this.resultsContainer.innerHTML = `<div class="cmd-no-results">No results found.</div>`;
            return;
        }

        let currentCategory = '';

        this.filteredItems.forEach((item, index) => {
            // Category Header
            if (item.category !== currentCategory) {
                currentCategory = item.category;
                const catHeader = document.createElement('div');
                catHeader.className = 'cmd-category';
                catHeader.innerText = currentCategory;
                this.resultsContainer.appendChild(catHeader);
            }

            const el = document.createElement('div');
            el.className = `cmd-item ${index === this.selectedIndex ? 'active' : ''}`;
            el.innerHTML = `
                <i class="${item.icon}"></i>
                <span>${item.title}</span>
                ${index === this.selectedIndex ? '<i class="fas fa-level-down-alt cmd-enter-icon"></i>' : ''}
            `;

            el.addEventListener('click', () => {
                item.action();
                this.close();
            });

            el.addEventListener('mouseenter', () => {
                this.selectedIndex = index;
                this.updateActiveItem();
            });

            this.resultsContainer.appendChild(el);
        });

        this.ensureVisible();
    }

    navigate(direction) {
        this.selectedIndex += direction;
        if (this.selectedIndex < 0) this.selectedIndex = this.filteredItems.length - 1;
        if (this.selectedIndex >= this.filteredItems.length) this.selectedIndex = 0;
        this.updateActiveItem();
        this.ensureVisible();
    }

    updateActiveItem() {
        const items = this.resultsContainer.querySelectorAll('.cmd-item');
        items.forEach((el, index) => {
            if (index === this.selectedIndex) {
                el.classList.add('active');
                if (!el.querySelector('.cmd-enter-icon')) {
                    el.innerHTML += '<i class="fas fa-level-down-alt cmd-enter-icon"></i>';
                }
            } else {
                el.classList.remove('active');
                const enterIcon = el.querySelector('.cmd-enter-icon');
                if (enterIcon) enterIcon.remove();
            }
        });
    }

    ensureVisible() {
        const activeEl = this.resultsContainer.querySelector('.cmd-item.active');
        if (activeEl) {
            activeEl.scrollIntoView({ block: 'nearest' });
        }
    }

    selectItem() {
        const item = this.filteredItems[this.selectedIndex];
        if (item) {
            item.action();
            this.close();
        }
    }
}

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    new CommandPalette();
});

// Enhanced Interactive Features for Leadership Portfolio

// ===== Page Loader Animation =====
window.addEventListener('load', () => {
    const loader = document.querySelector('.page-loader');
    if (loader) {
        // Remove artificial delay to make site load instantly
        loader.classList.add('fade-out');
        setTimeout(() => loader.remove(), 500);
    }
});

// Fallback: Force hide loader after 1 second (reduced from 2s)
setTimeout(() => {
    const loader = document.querySelector('.page-loader');
    if (loader && !loader.classList.contains('fade-out')) {
        loader.classList.add('fade-out');
        setTimeout(() => loader.remove(), 500);
    }
}, 1000);

// ===== Dark/Light Theme Toggle =====
// Theme toggle removed as per user request
/*
const themeToggle = document.getElementById('themeToggle');
const themeIcon = themeToggle.querySelector('i');

// Check for saved theme preference or default to light mode
const currentTheme = localStorage.getItem('theme') || 'light';
if (currentTheme === 'dark') {
    document.body.classList.add('dark-theme');
    themeIcon.classList.remove('fa-moon');
    themeIcon.classList.add('fa-sun');
}

// Theme toggle click handler
themeToggle.addEventListener('click', () => {
    document.body.classList.toggle('dark-theme');

    // Update icon
    if (document.body.classList.contains('dark-theme')) {
        themeIcon.classList.remove('fa-moon');
        themeIcon.classList.add('fa-sun');
        localStorage.setItem('theme', 'dark');
    } else {
        themeIcon.classList.remove('fa-sun');
        themeIcon.classList.add('fa-moon');
        localStorage.setItem('theme', 'light');
    }
});
*/


// ===== Mobile Navigation Toggle =====
const hamburger = document.querySelector('.hamburger');
const navMenu = document.querySelector('.nav-menu');
const navLinks = document.querySelectorAll('.nav-menu a');

if (hamburger) {
    hamburger.addEventListener('click', () => {
        navMenu.classList.toggle('active');
        hamburger.classList.toggle('active');

        // Animate hamburger to X
        const spans = hamburger.querySelectorAll('span');
        if (hamburger.classList.contains('active')) {
            spans[0].style.transform = 'rotate(45deg) translate(5px, 5px)';
            spans[1].style.opacity = '0';
            spans[2].style.transform = 'rotate(-45deg) translate(7px, -6px)';
        } else {
            spans[0].style.transform = 'none';
            spans[1].style.opacity = '1';
            spans[2].style.transform = 'none';
        }
    });
}

// Close mobile menu when clicking on a link
navLinks.forEach(link => {
    link.addEventListener('click', () => {
        // Don't close menu if clicking dropdown toggle
        if (!link.classList.contains('dropdown-toggle')) {
            navMenu.classList.remove('active');
            hamburger.classList.remove('active');
            const spans = hamburger.querySelectorAll('span');
            spans[0].style.transform = 'none';
            spans[1].style.opacity = '1';
            spans[2].style.transform = 'none';
        }
    });
});

// ===== Mobile Dropdown Toggle =====
const dropdownToggles = document.querySelectorAll('.dropdown-toggle');
dropdownToggles.forEach(toggle => {
    toggle.addEventListener('click', (e) => {
        e.preventDefault();
        const dropdown = toggle.closest('.dropdown');

        // On mobile, toggle the dropdown
        if (window.innerWidth <= 768) {
            dropdown.classList.toggle('active');
        }
    });
});

// ===== Smooth Scrolling =====
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            const navHeight = document.querySelector('.navbar').offsetHeight;
            const targetPosition = target.offsetTop - navHeight;

            window.scrollTo({
                top: targetPosition,
                behavior: 'smooth'
            });
        }
    });
});

// ===== Active Navigation on Scroll =====
const sections = document.querySelectorAll('section[id]');
const navItems = document.querySelectorAll('.nav-menu a');

function highlightNav() {
    let current = '';
    const scrollY = window.pageYOffset;

    sections.forEach(section => {
        // Adjusted offset for sticky navbar + clearer active state
        const sectionTop = section.offsetTop - 150;
        const sectionHeight = section.offsetHeight;

        if (scrollY >= sectionTop && scrollY < sectionTop + sectionHeight) {
            current = section.getAttribute('id');
        }
    });

    // Fallback for bottom of page (Contact)
    if ((window.innerHeight + window.scrollY) >= document.body.offsetHeight - 50) {
        current = 'contact';
    }

    navItems.forEach(item => {
        item.classList.remove('active');
        if (item.getAttribute('href') === `#${current}`) {
            item.classList.add('active');
        }
    });
}

window.addEventListener('scroll', highlightNav);

// ===== Scroll Indicator in Hero =====
const scrollIndicator = document.querySelector('.scroll-indicator');
if (scrollIndicator) {
    window.addEventListener('scroll', () => {
        if (window.scrollY > 100) {
            scrollIndicator.style.opacity = '0';
        } else {
            scrollIndicator.style.opacity = '1';
        }
    });
}

// ===== Intersection Observer for Fade-in Animations =====
const observerOptions = {
    threshold: 0.1,
    rootMargin: '0px 0px -50px 0px'
};

const fadeInObserver = new IntersectionObserver((entries) => {
    entries.forEach((entry, index) => {
        if (entry.isIntersecting) {
            setTimeout(() => {
                entry.target.classList.add('fade-in-visible');
            }, index * 100); // Staggered animation
            fadeInObserver.unobserve(entry.target);
        }
    });
}, observerOptions);

// Observe all sections and cards
document.querySelectorAll('section, .leadership-card, .cert-platform, .expertise-category, .pillar').forEach(el => {
    el.classList.add('fade-in');
    fadeInObserver.observe(el);
});

// ===== Parallax Effect on Hero =====
// Parallax removed to fix scroll overlap issues


// ===== Animated Gradient Orbs =====
function createOrbs() {
    const orbContainer = document.createElement('div');
    orbContainer.className = 'orb-container';
    document.body.appendChild(orbContainer);

    for (let i = 0; i < 3; i++) {
        const orb = document.createElement('div');
        orb.className = 'gradient-orb';
        orb.style.left = `${Math.random() * 100}%`;
        orb.style.top = `${Math.random() * 100}%`;
        orb.style.animationDelay = `${i * 2}s`;
        orbContainer.appendChild(orb);
    }
}

createOrbs();

// ===== Counter Animation for Stats =====
function animateCounter(element, target, duration = 2000) {
    let current = 0;
    const increment = target / (duration / 16);
    const timer = setInterval(() => {
        current += increment;
        if (current >= target) {
            element.textContent = target;
            clearInterval(timer);
        } else {
            element.textContent = Math.floor(current);
        }
    }, 16);
}

// Trigger counter animation when stats are visible
const statsObserver = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting && !entry.target.classList.contains('counted')) {
            entry.target.classList.add('counted');
            const value = entry.target.textContent.trim();

            if (value.includes('%')) {
                const num = parseInt(value);
                if (!isNaN(num)) {
                    animateCounter(entry.target, num);
                    setTimeout(() => {
                        entry.target.textContent = num + '%';
                    }, 2000);
                }
            } else if (value.includes('K') || value.includes('$')) {
                // Handle formats like "$55K+" or "55K" or "4x"
                const cleanValue = value.replace(/[$K+x]/g, '');
                const num = parseInt(cleanValue);
                if (!isNaN(num)) {
                    animateCounter(entry.target, num);
                    setTimeout(() => {
                        if (value.includes('$')) {
                            entry.target.textContent = '$' + num + 'K+';
                        } else if (value.includes('x')) {
                            entry.target.textContent = num + 'x';
                        } else {
                            entry.target.textContent = num + '%';
                        }
                    }, 2000);
                }
            }
        }
    });
}, { threshold: 0.5 });

document.querySelectorAll('.stat h3, .achievement-number').forEach(stat => {
    statsObserver.observe(stat);
});

// ===== Button Micro-animations =====
document.querySelectorAll('.btn').forEach(btn => {
    btn.addEventListener('mouseenter', function () {
        this.style.transform = 'translateY(-2px) scale(1.02)';
    });

    btn.addEventListener('mouseleave', function () {
        this.style.transform = 'translateY(0) scale(1)';
    });

    btn.addEventListener('mousedown', function () {
        this.style.transform = 'translateY(0) scale(0.98)';
    });

    btn.addEventListener('mouseup', function () {
        this.style.transform = 'translateY(-2px) scale(1.02)';
    });
});

// ===== Floating Animation for Certification Badges =====
const certBadges = document.querySelectorAll('.cert-icon, .hero-badge');
certBadges.forEach((badge, index) => {
    badge.style.animation = `float 3s ease-in-out ${index * 0.5}s infinite`;
});

// ===== Form Validation & Enhancement =====
const contactForm = document.querySelector('.contact-form form');
if (contactForm) {
    contactForm.addEventListener('submit', async (e) => {
        e.preventDefault();

        const submitBtn = contactForm.querySelector('button[type="submit"]');
        const originalText = submitBtn.textContent;

        // Show loading state
        submitBtn.textContent = 'Sending...';
        submitBtn.disabled = true;

        // If using Formspree, submit the form
        if (contactForm.action.includes('formspree')) {
            try {
                const response = await fetch(contactForm.action, {
                    method: 'POST',
                    body: new FormData(contactForm),
                    headers: {
                        'Accept': 'application/json'
                    }
                });

                if (response.ok) {
                    submitBtn.textContent = '✓ Message Sent!';
                    submitBtn.style.background = '#4ade80';
                    contactForm.reset();

                    setTimeout(() => {
                        submitBtn.textContent = originalText;
                        submitBtn.style.background = '';
                        submitBtn.disabled = false;
                    }, 3000);
                } else {
                    throw new Error('Form submission failed');
                }
            } catch (error) {
                submitBtn.textContent = '✗ Error - Try Again';
                submitBtn.style.background = '#ef4444';

                setTimeout(() => {
                    submitBtn.textContent = originalText;
                    submitBtn.style.background = '';
                    submitBtn.disabled = false;
                }, 3000);
            }
        } else {
            // Fallback for demo
            setTimeout(() => {
                submitBtn.textContent = '✓ Message Sent!';
                submitBtn.style.background = '#4ade80';
                contactForm.reset();

                setTimeout(() => {
                    submitBtn.textContent = originalText;
                    submitBtn.style.background = '';
                    submitBtn.disabled = false;
                }, 3000);
            }, 1000);
        }
    });
}

// ===== Make Credential Cards Clickable =====
document.querySelectorAll('.cert-platform').forEach(card => {
    const link = card.querySelector('a');
    if (link) {
        card.style.cursor = 'pointer';
        card.addEventListener('click', (e) => {
            if (e.target.tagName !== 'A') {
                link.click();
            }
        });
    }
});

// ===== Skip to Content Accessibility =====
const skipLink = document.querySelector('.skip-to-content');
if (skipLink) {
    skipLink.addEventListener('click', (e) => {
        e.preventDefault();
        const mainContent = document.querySelector('main') || document.querySelector('#home');
        if (mainContent) {
            mainContent.focus();
            mainContent.scrollIntoView({ behavior: 'smooth' });
        }
    });
}

// ===== Keyboard Navigation Enhancement =====
document.addEventListener('keydown', (e) => {
    // ESC to close mobile menu
    if (e.key === 'Escape' && navMenu.classList.contains('active')) {
        navMenu.classList.remove('active');
        hamburger.classList.remove('active');
    }
});

// ===== Scroll Progress Indicator =====
function updateScrollProgress() {
    const winScroll = document.body.scrollTop || document.documentElement.scrollTop;
    const height = document.documentElement.scrollHeight - document.documentElement.clientHeight;
    const scrolled = (winScroll / height) * 100;

    let progressBar = document.querySelector('.scroll-progress');
    if (!progressBar) {
        progressBar = document.createElement('div');
        progressBar.className = 'scroll-progress';
        document.body.appendChild(progressBar);
    }
    progressBar.style.width = scrolled + '%';
}

window.addEventListener('scroll', updateScrollProgress);

// ===== Enhanced Card Hover Effects =====
document.querySelectorAll('.leadership-card, .expertise-category, .cert-platform').forEach(card => {
    card.addEventListener('mouseenter', function () {
        this.style.transform = 'translateY(-10px) scale(1.02)';
    });

    card.addEventListener('mouseleave', function () {
        this.style.transform = 'translateY(0) scale(1)';
    });
});

// ===== Lazy Loading Images =====
if ('IntersectionObserver' in window) {
    const imageObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const img = entry.target;
                if (img.dataset.src) {
                    img.src = img.dataset.src;
                    img.removeAttribute('data-src');
                }
                imageObserver.unobserve(img);
            }
        });
    });

    document.querySelectorAll('img[data-src]').forEach(img => {
        imageObserver.observe(img);
    });
}

// ===== Console Welcome Message =====
console.log('%c👋 Welcome to Upendra Kumar\'s Portfolio!', 'color: #0078d4; font-size: 20px; font-weight: bold;');
console.log('%cAzure Solutions Architect | Seeking Leadership Roles', 'color: #50e6ff; font-size: 14px;');
console.log('%cInterested in collaboration? Let\'s connect!', 'color: #666; font-size: 12px;');

// ===== Performance Monitoring =====
if ('PerformanceObserver' in window) {
    const perfObserver = new PerformanceObserver((list) => {
        for (const entry of list.getEntries()) {
            if (entry.entryType === 'navigation') {
                console.log(`Page load time: ${entry.loadEventEnd - entry.fetchStart}ms`);
            }
        }
    });
    perfObserver.observe({ entryTypes: ['navigation'] });
}

console.log('🚀 Portfolio loaded successfully!');

// ===== Scroll to Top Logic =====
const scrollToTopBtn = document.getElementById('scrollToTop');

if (scrollToTopBtn) {
    // Show button when scrolling down
    window.addEventListener('scroll', () => {
        if (window.scrollY > 500) {
            scrollToTopBtn.classList.add('visible');
        } else {
            scrollToTopBtn.classList.remove('visible');
        }
    });

    // Scroll to top when clicked
    scrollToTopBtn.addEventListener('click', () => {
        window.scrollTo({
            top: 0,
            behavior: 'smooth'
        });
    });
}

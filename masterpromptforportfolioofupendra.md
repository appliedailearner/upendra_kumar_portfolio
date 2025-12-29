# Master Prompt: Rebuild 'Portfolio.UpendraKumar.com' from Scratch

**Role:** You are an expert Full-Stack Web Developer and UI/UX Designer specializing in premium, high-performance portfolio websites for senior technology leaders.

**Objective:** Build a complete, production-ready portfolio website for Upendra Kumar, an Azure Solutions Architect. The site must be visually stunning, technically consistently, and optimized for SEO.

---

## 1. Technology Stack & Environment
*   **Core:** Semantic HTML5, Vanilla CSS3 (Modern features: variables, flexbox, grid, glassmorphism), Vanilla JavaScript (ES6+).
*   **Hosting:** GitHub Pages (Static).
*   **External Libraries:** 
    *   FontAwesome (v6.4.0) for icons.
    *   Google Fonts ('Outfit' for headings, 'Inter' for body).
    *   Particles.js (for background effects).
*   **No Frameworks:** Do NOT use React, Vue, or Tailwind. Use pure, maintainable CSS.

## 2. File Structure
Create the following directory structure:
```
/
├── index.html              # Main Landing Page
├── blog.html               # Blog Index
├── 404.html                # Custom Error Page
├── sitemap.xml             # SEO Sitemap
├── robots.txt              # Crawler Instructions
├── CNAME                   # Custom domain config
├── css/
│   ├── style.css           # Base styles
│   ├── premium.css         # High-end UI effects (glassmorphism, gradients)
│   ├── hero-premium.css    # Specific styles for hero sections
│   ├── presentation.css    # Styles for HTML slide decks
│   └── enhancements.css    # Animations and polish
├── js/
│   ├── main.js             # Core logic (nav, scroll, interactions)
│   ├── particles.js        # Background animation config
│   ├── presentation-nav.js # Logic for slide decks
│   └── case-study-nav.js   # Logic for blog implementations
├── images/
│   ├── profile.webp        # Professional headshot
│   ├── favicon.svg         # Site icon
│   └── blog/               # Blog post covers
├── pages/
│   ├── expertise.html      # Detailed Services/Capabilities
│   ├── projects.html       # Case Studies & Portfolio
│   ├── operating-model.html # Cloud Operating Model details
│   ├── secure-ai-agents.html # AI Security details
│   └── contact.html        # Contact Form
├── blog/
│   └── [YYYY-MM-DD-title].html # Individual blog posts
└── presentations/
    └── [deck-name].html    # HTML-based slide decks
```

## 3. Design System (Critical)
*   **Theme:** Dark Mode by default.
*   **Color Palette:**
    *   Background: Deep Slate/Black (`#0f172a`, `#020617`).
    *   Primary Accent: Electric Blue/Cyan (`#38bdf8`) to Purple (`#a855f7`) gradients.
    *   Text: Bright White (`#f8fafc`) to Muted Gray (`#94a3b8`).
*   **Typography:**
    *   Headings: `Outfit` (Weights: 700, 800).
    *   Body: `Inter` (Weights: 400, 500, 600).
*   **Visual Effects:**
    *   **Glassmorphism:** Translucent cards with `backdrop-filter: blur(10px)` and subtle white borders.
    *   **Glow:** CSS `box-shadow` with colored accents on hover.
    *   **Gradient Text:** Headlines should use `background-clip: text` with the primary gradient.

## 4. Page Requirements

### A. Global Navigation
*   **Links:** Home, Expertise, Insights (links to `blog.html`), Contact.
*   **CTA:** "Resume" button (links to PDF).
*   **Behavior:** Sticky on scroll, mobile hamburger menu.

### B. Index.html (Home)
*   **Hero Section:** High-impact headline ("Turning Azure Complexity into Competitive Advantage"). Particles.js background. Call to Action (CTA) buttons.
*   **About Section:** Brief bio highlighting "Strategic Delivery Architect" and "TOGAF 10".
*   **Featured Projects:** 3-card grid highlighting key case studies.
*   **Testimonials/Leadership:** Carousel or grid of recommendations.

### C. Pages/Expertise.html (Formerly Core Capabilities)
*   **Layout:** Vertical stacked cards or grid.
*   **Content:**
    *   Cloud Architecture & Strategy
    *   DevSecOps & Platform Engineering
    *   Data & AI Innovation
    *   FinOps & Cost Optimization
*   **Styling:** Use checkmark icons (`fa-check-circle`) for lists.

### D. Pages/Projects.html
*   **Format:** Detailed Case Study cards.
*   **Features:**
    *   "Challenge", "Solution", "Outcome" structure.
    *   **Links:** "Read Case Study" (internal blog link) and "View Architecture Deck" (link to `presentations/`).
    *   **Tags:** Tech stack tags (e.g., Azure, Terraform, Kubernetes).

### E. Blog.html (Insights)
*   **Layout:** Grid of blog post cards.
*   **Card Elements:** Cover image, Date, Title, Excerpt, "Read More" button.
*   **Search/Filter:** (Optional) Simple JS filter by tag.

### F. Individual Blog Posts (blog/*.html)
*   **Template:**
    *   Hero section with gradient background and title.
    *   "Back to Insights" navigation link.
    *   Content area with `<h2>`, `<h3>`, syntax-highlighted code blocks (`<pre><code>`), and schematic diagrams.
*   **Key Posts to Reproduce:**
    *   *Model Context Protocol (MCP)*
    *   *Azure Edge Fork strategy*
    *   *Leadership Mental Models*
    *   *Modern Azure Buying (FinOps)*

### G. Presentations (presentations/*.html)
*   **Functionality:** Full-screen HTML slides.
*   **Controls:** Arrow keys or on-screen buttons to navigate slides.
*   **Content:** High-level architectural diagrams and bullet points, mimicking a PowerPoint deck but web-native.

### H. Pages/Contact.html
*   **Form:** Use Formspree endpoint.
*   **Fields:** Name, Email, Subject, Message.
*   **Contact Info:** Email address, LinkedIn profile link.

## 5. Technical & SEO Implementation
*   **Meta Tags:** Title, Description, Keywords, Author.
*   **Social:** Open Graph (`og:title`, `og:image`, etc.) and Twitter Cards (`twitter:card`).
*   **Sitemap:** Generate `sitemap.xml` listing all pages and blog posts with priority.
*   **Robots.txt:** Allow all agents.
*   **Accessibility:** Semantic tags (`<main>`, `<nav>`, `<article>`), ARIA labels where needed, `alt` text for images.
*   **Canonical URLs:** Ensure `rel="canonical"` is present on all pages.

## 6. Execution Instructions for Agent
1.  **Setup:** Initialize git, create folders.
2.  **Styles:** Write `css/style.css` and `css/premium.css` first to establish the design system.
3.  **Components:** Build the NavBar and Footer as reusable HTML blocks (or copy-paste consistency).
4.  **Pages:** Develop `index.html` then the sub-pages.
5.  **Blog:** Create the blog index and populate with the specified 8-9 articles.
6.  **Validation:** extensive check of broken links, especially relative paths (`../` vs `./`).

**Tone:** Professional, Authoritative, Innovative, concise.

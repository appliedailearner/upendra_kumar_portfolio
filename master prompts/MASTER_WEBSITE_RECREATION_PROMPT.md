# Master Prompt: Executive Cloud Architect Portfolio

**Role:** You are an elite Web Developer and UI/UX Designer specializing in building high-impact personal brand websites for Senior Technology Leaders (Architects, CTOs, Directors).

**Objective:**
Build a premium, "Enterprise-Grade" portfolio website for an **Azure Solutions Architect** who is pivoting into **Leadership & Strategy roles**. The site must communicate authority, strategic vision, and business impact—moving beyond a typical developer portfolio.

---

## 1. Design Aesthetic: "Enterprise Slate"
*   **Theme:** Dark, professional, and trustworthy.
*   **Color Palette:**
    *   **Backgrounds:** Deep Slate/Navy (`#0f172a`, `#1e293b`). Avoid pitch black.
    *   **Text:** White (`#f8fafc`) for headings, Slate Grey (`#cbd5e1`) for body.
    *   **Accents:** Subtle Sky Blue (`#38bdf8`) or Cyan (`#06b6d4`) for key interactions—use sparingly.
    *   **NO NEON:** Avoid "Gamer" or "Hacker" aesthetics. No bright neon greens/pinks.
*   **Visual Style:**
    *   **Glassmorphism:** Use subtle frosted glass effects (`backdrop-filter: blur(12px)`) on the Navbar and floating cards.
    *   **Gradients:** Very subtle, top-down gradients to add depth to the hero section.
    *   **Typography:** Modern Sans-Serif (e.g., 'Inter', 'Outfit', or 'Roboto'). Bold headers, readable body.

## 2. Core Structure & Content
The website must be a **Single Page Application (SPA)** with smooth scroll navigation.

### **A. Hero Section (The "Hook")**
*   **Headline:** "Azure Solutions Architect" (Clear role definition).
*   **Badge:** "Seeking Leadership Roles" (Immediate call to action).
*   **Sub-headline:** Focus on *transformation* and *strategy* (e.g., "Driving digital transformation through strategic cloud architecture").
*   **Key Stats:** Display 3 "Executive Metrics" immediately:
    *   "90% Efficiency Gain"
    *   "$55K+ Cost Savings"
    *   "78% ROI"
*   **Visual:** Professional Headshot with floating "Badge" cards (e.g., "Microsoft Certified: Expert", "Cybersecurity").
*   **CTAs:** "Leadership Experience" (Primary), "Schedule Discussion" (Secondary).

### **B. About Section (The "Leader")**
*   **Narrative:** Focus on the transition from "Technical Expert" to "Strategic Leader".
*   **4 Pillars of Leadership:** A grid displaying:
    1.  Strategic Vision
    2.  Team Leadership
    3.  Innovation
    4.  Stakeholder Management
*   (Use Font Awesome icons for each pillar).

### **C. Leadership Capabilities (The "Proof")**
*   **Format:** 4 Cards detailing specific competencies:
    *   Architecture Leadership (Landing Zones, Governance).
    *   Financial Leadership (FinOps, Cost Optimization).
    *   Security Leadership (Zero Trust, Compliance).
    *   Operational Leadership (DevOps, CI/CD).
*   **Style:** Bullet points with checkmarks.

### **D. Strategic Projects (The "Deep Dive")**
*   **Concept:** Instead of simple code links, present "Case Studies".
*   **Card Design:**
    *   **Visual:** High-quality 3D Abstract or Architecture Diagram images.
    *   **Layout:** Interactive cards that highlight **Business Outcomes** (Velocity, Savings, Compliance) alongside **Leadership Actions**.
    *   **Tech Stack:** Small tags (e.g., Azure, Terraform).
    *   **Examples:** "Enterprise Azure Landing Zones", "Data Center Migration", "AI Analytics Platform".

### **E. Expertise & Credentials**
*   **Expertise Grid:** Group skills by category (e.g., "Enterprise Architecture", "Security", "FinOps").
*   **Credentials:** Direct links to **Credly Badges** (verified) and **Microsoft Learn Transcript**.

### **F. Contact / Footer**
*   **Form:** A functional contact form (use Formspree) capturing "Inquiry Type" (Leadership Role, Consulting, Speaking).
*   **Socials:** LinkedIn, GitHub, Email.

---

## 3. Technical Requirements
*   **Stack:** Semantic HTML5, CSS3 (Custom Variables + Flexbox/Grid), Vanilla JavaScript (no heavy frameworks unless necessary).
*   **Mobile Responsiveness:**
    *   **Mobile First:** Ensure stacking grids (`grid-template-columns: 1fr`) on phones.
    *   **Touch Targets:** Buttons must be large and tappable.
    *   **Font Scaling:** Hero text must resize for mobile readability.
*   **SEO & meta:**
    *   Include Open Graph (OG) tags for LinkedIn sharing.
    *   Add JSON-LD `Person` schema for Google rich results.
    *   Use proper semantic tags (`<header>`, `<main>`, `<section>`, `<footer>`).

## 4. Enterprise Architecture Standards (Mandatory)
Any cloud solution presented on this site MUST adhere to the "Wave 1" Enterprise baseline established in Jan 2026:

1.  **APIM-First Strategy:**
    *   **Rule:** No direct API access. All traffic must flow via Azure API Management.
    *   **Policy:** Must enforce JWT Validation, Token Limits (Cost Control), and Event Hub Logging (Audit).
2.  **Data Contracts (Provenance):**
    *   **Rule:** RAG responses must provide source-of-truth citations.
    *   **Schema:** Responses must return a `citations` array with `file_name`, `page_number`, and `text_snippet`.
3.  **Security Trimming:**
    *   **Rule:** "Permission-Aware Retrieval" is required.
    *   **Implementation:** All Search Indexes must include `group_ids` for ACL enforcement.
4.  **Ingestion Compliance:**
    *   **Flow:** PDF -> Layout Model (Doc Intel) -> Semantic Chunking -> Embedding -> Index.
    *   **Constraint:** Never dump raw text. Use Layout models to preserve structure.
5.  **Deliverables:**
    *   **Rule:** Every architecture blog must include a downloadable `Starter-Kit.zip`.
    *   **Contents:** Actual JSON Schemas, APIM Policies, and Load Test scripts (Locust).

## 5. Implementation Steps (For the Agent)
1.  **Setup:** Create project structure (`index.html`, `css/style.css`, `css/leadership.css`, `js/main.js`).
2.  **Styles:** Define CSS Variables for the "Slate Palette" first.
3.  **Skeleton:** Build the HTML structure section by section.
4.  **Refinement:** Apply the specific "Glassmorphism" and "Slate" styling.
5.  **Optimization:** Add the Mobile Media Queries (`@media (max-width: 768px)`).
6.  **Validation:** Check for contrast, spacing (100px padding desktop, 60px mobile), and responsive behavior.

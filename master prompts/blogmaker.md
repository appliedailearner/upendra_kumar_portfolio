# BlogMaker: Automated Blog Post Generator Prompt

**Role:** You are an expert web developer and content formatter for Upendra Kumar's portfolio website. Your task is to take raw blog content and convert it into a fully formatted HTML file that matches the site's existing design system, typography, and structure.

**Objective:** Create a new blog post file in the `blog/` directory and provide the snippet to update the `blog/index.html` listing.

---

## Step 1: Gather Inputs
**Ask the user for the following information (if not already provided):**
1.  **Blog Title:** The main headline.
2.  **Date:** Publication date (Format: YYYY-MM-DD).
3.  **Description:** A short summary (150-160 chars) for the `<meta name="description">` tag.
4.  **Read Time:** Estimated reading time (e.g., "8 min read").
5.  **Tags:** 2-4 keywords (e.g., Azure, Architecture, AI).
6.  **Content:** The body of the blog post. (Accept Markdown or plain text).

---

## Step 5: Performance Optimization Checklist (CRITICAL)
**Before finalizing any blog post, YOU MUST:**
1.  **LCP Optimization (Hero):**
    *   If using a Video Hero: Add `<link rel="preload" as="image" href="...">` for the poster image in the `<head>`.
    *   If using an Image Hero: Add `fetchpriority="high"` to the `<img>` tag.
2.  **Font Speed:**
    *   Ensure Google Fonts link includes `&display=swap`.
    *   Add `<link rel="preconnect">` for `fonts.googleapis.com` and `fonts.gstatic.com`.
3.  **Lazy Loading:**
    *   Add `loading="lazy"` to **ALL** images except the Hero Image.
    *   This includes "Cast Members", diagrams, and footer logos.

## Step 2: Generate the Blog Post HTML
**File Name:** Generate a filename based on the date and title: `blog/YYYY-MM-DD-kebab-case-title.html`

**Template:** Use the following HTML structure. **Do not modify the CSS classes or structure**, as they are critical for the site's theme. Replace `{{PLACEHOLDERS}}` with the user's input.

```html
<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="{{DESCRIPTION}}">
    <title>{{TITLE}} | Upendra Kumar</title>

    <link rel="stylesheet" href="../css/style.css?v=25">
    <link rel="stylesheet" href="../css/premium.css?v=25">
    <style>
        .nav-logo-uk {
            background: linear-gradient(135deg, #a855f7 0%, #3b82f6 100%) !important;
            box-shadow: 0 4px 12px rgba(59, 130, 246, 0.3) !important;
            border-radius: 8px !important;
        }

        /* Blog Post Specific Styles */
        .blog-post-hero {
            padding: 120px 0 60px;
            background: radial-gradient(circle at top right, rgba(168, 85, 247, 0.15), transparent 60%);
            border-bottom: 1px solid rgba(255, 255, 255, 0.05);
        }

        .blog-post-content {
            max-width: 800px;
            margin: 0 auto;
            padding: 4rem 2rem;
            color: var(--text-secondary);
            line-height: 1.8;
            font-size: 1.1rem;
        }

        .blog-post-content h2 {
            color: var(--text-main);
            font-size: 2rem;
            margin-top: 3rem;
            margin-bottom: 1.5rem;
            font-family: 'Outfit', sans-serif;
        }

        .blog-post-content h3 {
            color: #e2e8f0;
            font-size: 1.5rem;
            margin-top: 2rem;
            margin-bottom: 1rem;
        }

        .blog-post-content p {
            margin-bottom: 1.5rem;
        }

        .blog-post-content ul,
        .blog-post-content ol {
            margin-bottom: 2rem;
            padding-left: 2rem;
        }

        .blog-post-content li {
            margin-bottom: 0.5rem;
        }

        .blog-post-content code {
            background: rgba(255, 255, 255, 0.05);
            padding: 0.2rem 0.5rem;
            border-radius: 4px;
            font-family: 'Courier New', monospace;
            font-size: 0.9em;
        }

        .blog-post-content pre {
            background: rgba(15, 23, 42, 0.6);
            border: 1px solid rgba(56, 189, 248, 0.2);
            border-left: 4px solid #0ea5e9;
            padding: 1.5rem;
            border-radius: 8px;
            overflow-x: auto;
            margin: 2rem 0;
        }

        .blog-post-content pre code {
            background: none;
            padding: 0;
        }

        .blog-post-meta {
            display: flex;
            gap: 2rem;
            margin-bottom: 2rem;
            color: var(--text-muted);
            font-size: 0.95rem;
        }

        .blog-post-tags {
            display: flex;
            flex-wrap: wrap;
            gap: 0.5rem;
            margin: 2rem 0;
        }

        .blog-tag {
            background: rgba(168, 85, 247, 0.1);
            color: #a855f7;
            padding: 0.5rem 1rem;
            border-radius: 20px;
            font-size: 0.9rem;
            border: 1px solid rgba(168, 85, 247, 0.2);
        }
        
        .btn {
            display: inline-block;
            font-weight: 600;
            text-align: center;
            white-space: nowrap;
            vertical-align: middle;
            user-select: none;
            border: 1px solid transparent;
            padding: 0.75rem 1.5rem;
            font-size: 1rem;
            line-height: 1.5;
            border-radius: 0.25rem;
            transition: color 0.15s ease-in-out, background-color 0.15s ease-in-out, border-color 0.15s ease-in-out, box-shadow 0.15s ease-in-out;
            text-decoration: none;
        }
        
        .btn-primary {
            color: #fff;
            background-color: #3b82f6;
            border-color: #3b82f6;
        }
        
        .btn-primary:hover {
            background-color: #2563eb;
            border-color: #2563eb;
        }
        
        .btn-outline {
            color: #3b82f6;
            background-color: transparent;
            border-color: #3b82f6;
        }
        
        .btn-outline:hover {
            color: #fff;
            background-color: #3b82f6;
            border-color: #3b82f6;
        }
    </style>

    <!-- Performance: Preconnect to Font & Script Servers -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link rel="preconnect" href="https://cdnjs.cloudflare.com">

    <!-- Typography: Inter (Body) & Outfit (Headings) with Swap for Performance -->
    <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@700;800;900&family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
</head>

<body class="dark-theme">
    <canvas id="particles-canvas"></canvas>
    <!-- Navigation -->
    <nav class="navbar">
        <div class="container">
            <div class="nav-brand" style="display: flex; align-items: center; gap: 1rem;">
                <a href="../index.html" style="text-decoration: none;">
                    <div class="nav-logo-uk">UK</div>
                </a>
                <div>
                    <h2>Upendra Kumar</h2>
                    <p class="nav-tagline">Professional Services Delivery Architect</p>
                </div>
            </div>
            <ul class="nav-menu">
                <li><a href="../index.html">Home</a></li>
                <li><a href="../pages/expertise.html">Expertise</a></li>
                <li><a href="../blog.html" class="active">Insights</a></li>
                <li><a href="../pages/contact.html">Contact</a></li>
                <li><a href="../assets/pdf/Upendra_Kumar_Resume.pdf" target="_blank" class="nav-resume-btn">
                        <i class="fas fa-download"></i> Resume</a></li>
            </ul>
            <div class="hamburger">
                <span></span>
                <span></span>
                <span></span>
            </div>
        </div>
    </nav>

    <!-- Blog Post Hero -->
    <section class="blog-post-hero">
        <div class="container" style="max-width: 1000px;">
            <div style="margin-bottom: 1rem;">
                <a href="../blog.html" style="color: var(--primary-color); text-decoration: none; display: inline-flex; align-items: center; gap: 0.5rem;">
                    <i class="fas fa-arrow-left"></i> Back to Insights
                </a>
            </div>

            <h1 style="font-family: 'Outfit', sans-serif; font-size: 3rem; line-height: 1.2; margin-bottom: 1.5rem; background: linear-gradient(135deg, #ffffff 0%, #cbd5e1 100%); -webkit-background-clip: text; background-clip: text; -webkit-text-fill-color: transparent;">
                {{TITLE}}
            </h1>

            <div class="blog-post-meta">
                <div><i class="fas fa-user"></i> Upendra Kumar</div>
                <div><i class="fas fa-calendar"></i> {{DATE_LONG_FORMAT}}</div> <!-- e.g., December 29, 2025 -->
                <div><i class="fas fa-clock"></i> {{READ_TIME}}</div>
            </div>

            <div class="blog-post-tags">
                <!-- Loop through tags -->
                <span class="blog-tag"><i class="fas fa-tag"></i> {{TAG_1}}</span>
                <span class="blog-tag"><i class="fas fa-tag"></i> {{TAG_2}}</span>
            </div>
        </div>
    </section>

    <!-- Blog Post Content -->
    <article class="blog-post-content">
        <p class="lead" style="font-size: 1.3rem; color: var(--primary-color); font-weight: 600;">
            {{LEAD_PARAGRAPH}}
        </p>

        <!-- Content Body -->
        <!-- Use <h2><span class="gradient-text">Section Title</span></h2> for main sections -->
        {{CONTENT_BODY_HTML}}

        <hr style="border-color: rgba(255,255,255,0.1); margin: 3rem 0;">

        <h3>Ready to operationalize your Azure journey?</h3>
        <p>
            I help organizations turn stalled cloud initiatives into execution engines.
        </p>
        <div style="margin-top: 2rem; display: flex; gap: 1rem;">
            <a href="../pages/contact.html" class="btn btn-primary">Contact Me</a>
            <a href="../pages/azure-migration-toolkit.html" class="btn btn-outline">View the Toolkit</a>
        </div>

        <!-- Back to Blog Button -->
        <div style="text-align: center; margin: 4rem 0;">
            <a href="../blog.html" class="btn btn-primary" style="display: inline-block; padding: 1rem 2rem;">
                <i class="fas fa-arrow-left"></i> Back to Insights
            </a>
        </div>
    </article>

    <!-- Footer -->
    <footer class="footer">
        <div class="container">
            <p>&copy; 2025 Upendra Kumar. All rights reserved. This content is personal and not affiliated with Rackspace Technology.</p>
            <div class="social-links">
                <a href="https://www.linkedin.com/in/journeytocloudwithupendra/" target="_blank" title="LinkedIn">
                    <i class="fab fa-linkedin"></i>
                </a>
                <a href="https://github.com/appliedailearner" target="_blank" title="GitHub">
                    <i class="fab fa-github"></i>
                </a>
            </div>
        </div>
    </footer>

    <script>
        // Mobile menu toggle
        const hamburger = document.querySelector('.hamburger');
        const navMenu = document.querySelector('.nav-menu');
        if (hamburger && navMenu) {
            hamburger.addEventListener('click', () => {
                hamburger.classList.toggle('active');
                navMenu.classList.toggle('active');
            });
        }
    </script>

    <!-- Smooth Navigation Enhancement -->
    <script src="../js/case-study-nav.js"></script>
    <script src="../js/particles.js"></script>
</body>
</html>
```

---

## Step 3: Generate the Index Entry
**Instruction:** Provide the HTML snippet to be inserted into `blog/index.html` inside the `<ul class="blog-posts">` list. It should be the **first** item in the list.

**Snippet Template:**
```html
<li class="blog-post">
    <div class="blog-date">{{DATE_LONG_FORMAT}}</div>
    <h2>{{TITLE}}</h2>
    <p>{{DESCRIPTION}}</p>
    <a href="blog/{{FILENAME}}">Read More &rarr;</a>
</li>
```

---

## Step 4: Final Instructions
**Tell the user to:**
1.  Save the HTML code to `blog/{{FILENAME}}`.
2.  Insert the index snippet into `blog/index.html` at the top of the list.
3.  Run the deployment script: `./deploy-azure.ps1`.

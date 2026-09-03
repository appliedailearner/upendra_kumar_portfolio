# upendra_kumar_portfolio

Source repository for **[portfolio.upendrakumar.com](https://portfolio.upendrakumar.com)** — the
personal portfolio, blog, and architecture-deck site of Upendra Kumar.

## Repository layout

| Path | What lives here |
|------|-----------------|
| **`site/`** | **The deployable website.** Everything under here — and only this — is published. `index.html`, `blog/`, `pages/`, `presentations/`, `css/`, `js/`, `images/`, `assets/`, `docs/`, `toolkits/`, plus `CNAME`, `robots.txt`, `sitemap.xml`, `feed.xml`, `status.json`. |
| `career/` | Résumé, executive bio, one-pagers, LinkedIn assets, career-planning notes, job tracker. |
| `tools/` | Automation. `content/` — blog/deck/infographic generators and prompts; `media/` — image conversion & optimization; `deploy/` — Azure/analytics deploy scripts; `qa/` — link/UI test scripts; `scripts/` — diagram & misc generators. |
| `project-docs/` | Project documentation, design-decision notes, deployment/DNS guides, status reports. |
| `labs/` | Standalone Azure lab / demo projects and git submodules referenced from the site's project write-ups. Not part of the published site. |
| `archive/` | Regenerable or stale artifacts kept for reference — Lighthouse reports, old screenshots, backups, scratch notes. Safe to prune. |

## Build & deploy

The site is deployed to GitHub Pages by [`.github/workflows/deploy.yml`](.github/workflows/deploy.yml)
on every push to `main`. The workflow publishes the **`site/`** directory only
(`upload-pages-artifact` with `path: 'site'`).

CSS is generated with Tailwind (`tailwind.config.js`, `package.json`); the compiled output is
committed at `site/css/tailwind-output.css`.

To preview locally:

```powershell
cd site
python -m http.server 8000
# open http://localhost:8000
```

## Submodules

`labs/` contains git submodules (see `.gitmodules`). To populate them:

```powershell
git submodule update --init --recursive
```

> Note: `labs/tmp-apim-samples` is a bare gitlink with no `.gitmodules` entry (pre-existing) and will
> not initialize.

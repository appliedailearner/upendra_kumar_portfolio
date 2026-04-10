# Agent Skills Integration Guide

This project now supports **Agent Skills**—modular expertise packages that provide AI assistants (like Antigravity) with structured knowledge about Azure architecture, ROI-focused content, and enterprise standards.

## 📂 Directory Structure
The skills are located in:
`c:\MyResumePortfolio\.agent\skills\`

Each skill is a subfolder containing:
- `SKILL.md`: The core instructions for the AI.
- `scripts/`: (Optional) Helper scripts.
- `resources/`: (Optional) Additional documentation or templates.

## 🚀 How to Add/Update Skills
1.  **Source:** Visit the [Agent-Skills Repository](https://github.com/appliedailearner/Agent-Skills).
2.  **Download:** Clone or download the repository.
3.  **Install:** Copy the desired skill folders (e.g., `azure-functions`, `azure-landing-zones`) from the `skills/` directory of the repo into your project's `.agent/skills/` directory.
    - **Correct Path:** `.agent/skills/azure-functions/SKILL.md`
    - **Incorrect Path:** `.agent/skills/skills/azure-functions/SKILL.md`

## 🧠 How it Works
When you use a "Master Prompt" (like `blogmaker.md` or the Portfolio Master Prompt), the AI is now instructed to skip to the `.agent/skills` folder first. 

- **Azure Knowledge:** If a skill for a specific Azure service is present, the AI will use it to ensure your blog posts and architecture diagrams follow current Microsoft best practices.
- **ROI & Value:** Skills help the AI maintain the "Cloud Practice Director" persona by providing ROI metrics and strategic alignment logic.

## 🛠️ Syncing Skills
To keep your skills up to date, you can periodically re-download the latest versions from the GitHub repository.

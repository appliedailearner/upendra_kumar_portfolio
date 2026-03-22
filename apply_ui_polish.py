import re
import os

html_path = r"C:\MyResumePortfolio\blog\2026-03-21-ai-compliance-gap.html"
with open(html_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Grid Shift
content = content.replace("grid-template-columns: 1fr 1fr;", "grid-template-columns: 0.8fr 1.2fr;", 1)

# 2. Card Padding
content = content.replace("padding: 3rem 2rem;", "padding: 2rem 2.5rem;")

# 3. Dynamic Glow & Glow Cleanup
active_css_old = """.pillar-feature-card.active {
            opacity: 1;
            transform: scale(1);
            border-color: rgba(56, 189, 248, 0.4);
            background: rgba(30, 41, 59, 0.6);
            box-shadow: 0 0 30px rgba(56, 189, 248, 0.1);
        }"""
        
active_css_new = """.pillar-feature-card.active {
            opacity: 1;
            transform: scale(1);
            background: rgba(30, 41, 59, 0.6);
        }
        .pillar-feature-card[data-pillar="p"].active { border-color: rgba(56, 189, 248, 0.5); box-shadow: 0 0 30px rgba(56, 189, 248, 0.15); }
        .pillar-feature-card[data-pillar="r"].active { border-color: rgba(168, 85, 247, 0.5); box-shadow: 0 0 30px rgba(168, 85, 247, 0.15); }
        .pillar-feature-card[data-pillar="o"].active { border-color: rgba(52, 211, 153, 0.5); box-shadow: 0 0 30px rgba(52, 211, 153, 0.15); }
        .pillar-feature-card[data-pillar="f"].active { border-color: rgba(251, 191, 36, 0.5); box-shadow: 0 0 30px rgba(251, 191, 36, 0.15); }"""
        
if active_css_old in content:
    content = content.replace(active_css_old, active_css_new)
else:
    print("Could not find the old active CSS block to replace.")

# 4. Architect Pulse CSS
pulse_css = """
        /* Architect Pulse Premium Alert */
        .architect-pulse {
            background: linear-gradient(90deg, rgba(239, 68, 68, 0.1) 0%, rgba(30, 41, 59, 0) 100%);
            border-left: 4px solid #ef4444;
            padding: 1.5rem;
            border-radius: 0 12px 12px 0;
            display: flex;
            align-items: center;
            gap: 1.5rem;
            opacity: 0.9;
            margin-top: 2rem;
        }
        .architect-pulse .pulse-icon {
            font-size: 2rem;
            color: #ef4444;
        }
        .architect-pulse p {
            margin: 0;
            font-size: 1.05rem;
            font-style: italic;
            color: #f8fafc;
            line-height: 1.6;
        }
"""

if "/* Architect Pulse Premium Alert */" not in content:
    content = content.replace("    </style>", pulse_css + "\n    </style>")

# 5. Architect Pulse HTML Restructure
html_old = """<div class="architect-pulse">\n            <p>\n                <i class="fas fa-exclamation-triangle pulse-icon"></i>\n                "A private path without strong identity is still weak. Proof requires both working in sync."\n            </p>\n        </div>"""
        
html_new = """<div class="architect-pulse">\n            <i class="fas fa-exclamation-triangle pulse-icon"></i>\n            <p>"A private path without strong identity is still weak. Proof requires both working in sync."</p>\n        </div>"""
        
content = content.replace(html_old, html_new)

with open(html_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Applied UI/UX polish to HTML.")

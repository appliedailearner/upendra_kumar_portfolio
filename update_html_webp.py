import re
import os

html_path = r"C:\MyResumePortfolio\blog\2026-03-21-ai-compliance-gap.html"
with open(html_path, 'r', encoding='utf-8') as f:
    content = f.read()

replacements = {
    'hero_chaos.png': 'hero_chaos.webp',
    'agent_mediation_layer.jpg': 'agent_mediation_layer.webp',
    'ai-landing-zone-vnet.png': 'ai-landing-zone-vnet.webp',
    'four_pillars_of_proof.png': 'four_pillars_of_proof.webp'
}

for old, new in replacements.items():
    content = content.replace(old, new)

with open(html_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Updated HTML references to WebP.")

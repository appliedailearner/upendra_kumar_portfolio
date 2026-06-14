import re

html_path = r"C:\MyResumePortfolio\blog\2026-03-21-ai-compliance-gap.html"
with open(html_path, 'r', encoding='utf-8') as f:
    content = f.read()

replacement = """        .pillars-split-container {
            display: grid;
            grid-template-columns: 0.8fr 1.2fr;
            gap: 4rem;
            margin: 6rem 0;
            align-items: start;
            position: relative;
            /* Breakout of 800px wrapper */
            width: 100vw;
            max-width: 1200px;
            margin-left: 50%;
            transform: translateX(-50%);
            padding: 0 2rem;
            box-sizing: border-box;
        }"""

# Using regex to match regardless of exact spacing
pattern = re.compile(r'\.pillars-split-container\s*\{\s*display:\s*grid;\s*grid-template-columns:\s*0\.8fr\s*1\.2fr;\s*gap:\s*4rem;\s*margin:\s*6rem\s*0;\s*align-items:\s*start;\s*position:\s*relative;\s*\}')

if pattern.search(content):
    content = pattern.sub(replacement, content)
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Fixed CSS properly.")
else:
    print("Could not find the target CSS to replace.")

import re

file_path = r'c:\MyResumePortfolio\blog\2026-05-20-the-enterprise-ai-model-layer-azure-model-router.html'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

font_links = '''
    <!-- Google Fonts - Premium Typography -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@700;800;900&display=swap" rel="stylesheet">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">
'''

if 'fonts.googleapis.com' not in content:
    content = content.replace('<title>', font_links + '\n    <title>')

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print('Added Google Fonts to blog post')
